# %%
import os

os.environ["MKL_NUM_THREADS"] = "4"
os.environ["NUMEXPR_NUM_THREADS"] = "4"
os.environ["OMP_NUM_THREADS"] = "4"
from statsmodels.base.model import GenericLikelihoodModel
from scipy.stats import norm
import pandas as pd
import pyhdfe
import numpy as np
import statsmodels.api as sm
from itertools import starmap
from functools import partial, reduce
from patsy import dmatrix, dmatrices
np.errstate(all="raise")
import functools
import statsmodels.formula.api as smf
from linearmodels import PanelOLS


def get_mle_betas(res, regimes):

    beta0_mle = res.params[0:regimes]

    beta1_mle = res.params[regimes : 2 * regimes]

    return beta0_mle, beta1_mle, np.append(beta0_mle, beta1_mle)


def get_mle_sigmas(res, regimes):
    """
    Get sigmas from MLE estimation, then transform back (take absolute value)
    """

    return np.abs(res.params[2 * regimes : 3 * regimes])
class DriverSpecificProbUberMLE(GenericLikelihoodModel):
    """An Uber MLE with two things different:
    - Gets rid of lambda as parameters
    - Uses driver-specific probabilities in likelihood
    - Uses bounding and constrained optimization for probabilities
    
    Uses full probabilities in classifier cols, not categoricals
    """
    
    def __init__(self, 
                 data,
                 classifier_pred, 
                 classifier_ind, 
                 regime_formulas,
                 covariate_formula=None,
                 hdfe=False,
                 entity_effects = False,
                 old_entity_effects=False,
                 time_effects = False,
                 drop_singletons = True,
                 same_impact=False,
                 overall_demean = False,
                 twoway_fixed_effects = 'dummy',
                 endog_data=None,
                 exog_data=None,
                 **kwargs):
        
        print("Initializing...")
        super().__init__(endog =np.ones((exog_data.shape[0], 1)), exog= np.ones((exog_data.shape[0],2)), **kwargs)
        
        self.df_model = exog_data.shape[1]
        self.df_resid = exog_data.shape[0] - exog_data.shape[1] + 1

        self.classifier_pred = classifier_pred
        self.classifier_ind = classifier_ind
        self.old_entity_effects = old_entity_effects
        self.n_regimes = len(classifier_ind)

        self.entity_effects = entity_effects
        self.time_effects = time_effects
        self.overall_demean = overall_demean
        self.twoway_fixed_effects = twoway_fixed_effects
        self.hdfe = hdfe
        self.regime_formulas = regime_formulas
        self.covariate_formula = covariate_formula
        
        if self.entity_effects or time_effects:    
            # Check for multiindex
            if not isinstance(data.index, pd.MultiIndex):
                raise Exception("Dataframe not a multi-index")
            
        if drop_singletons:
            # drop singleton observations...
            print("Dropping singleton observations...")
            
            self.df = self._drop_singletons(data=data)
        else:
            self.df = data
        
        self._entity = self.df.index.names[0]
        self._time = self.df.index.names[1]
            
        if self.entity_effects and self.time_effects:
            if len(self.df.index.get_level_values(0).value_counts().unique()) > 1 and self.overall_demean:
                print("Unbalanced Panel... Results with overall demean may not be correct...")
                
        if self.overall_demean and not (self.entity_effects and self.time_effects):
            raise Exception("Cannot calculate overall mean when two-way fixed effects not chosen")
    
        # get number of covariates
        try:
            self.num_covariates = self.covariates.shape[1]
        except AttributeError:
            self.num_covariates = 0
        
        self.num_regime_vars = self.regime_list.shape[2]-1
        
        self.same_impact = same_impact
        
        if not hdfe and self.time_effects and self.twoway_fixed_effects=='dummy':
            # get dummies for time variable
            self.covariates = self.covariates.reset_index(1).pipe(pd.get_dummies, columns=['date'])
    
    @functools.cached_property
    def regime_list(self):
        
        rl = [dmatrices(r, 
                        data = self.df, 
                        eval_env=1, 
                        return_type='dataframe')\
            for r in self.regime_formulas]
        
        if self.hdfe:
            # Create HDFE algorithm object
            algo = pyhdfe.create(self.df.index.to_frame().values)
            
            rl = [(pd.DataFrame(data = algo.residualize(y), columns = y.columns, index = y.index),
                                 pd.DataFrame(data = algo.residualize(X), columns = X.columns, index = X.index)) \
                                     for y,X in rl]
        else:
            if self.old_entity_effects:
                rl = [(y - y.groupby(level=0).transform('mean'), 
                        (X - X.groupby(level=0).transform('mean'))) \
                            for y, X in rl]
            if self.entity_effects:                
                e_mean = [(y.groupby(level=0).transform('mean'), 
                                    (X.groupby(level=0).transform('mean'))) \
                                        for y, X in rl]
            else:
                e_mean = [(0, (0)) for y, X in rl]
                
            if self.time_effects and self.twoway_fixed_effects == 'demean':
                
                t_mean = [(y.groupby(level=1).transform('mean'), 
                        (X.groupby(level=1).transform('mean'))) \
                                        for y, X in rl]
            else:
                t_mean = [(0, (0)) for y, X in rl]
            if self.overall_demean:
                overall_mean = [(y.groupby(level=[0,1]).transform('mean'), 
                                    (X.groupby(level=[0,1]).transform('mean'))) \
                                        for y, X in rl]
            else:
                overall_mean = [(0, (0)) for y, X in rl]
                
            rl = [(y - e_y - t_y + o_y, 
                    (X - e_x - t_x + o_x)) \
                            for (y, X), (e_y, e_x), (t_y, t_x), (o_y, o_x) \
                                in zip(rl, e_mean, t_mean, overall_mean)]
            
        # Turn rl into a 3D matrix
        return np.array([y.merge(X, left_index=True, right_index=True).values for y,X in rl])

    @functools.cached_property
    def covariates(self):
        if self.covariate_formula is None:
            self.covariate_names = []
            return ''
        else:
            c = dmatrix('-1 + ' + self.covariate_formula, 
                                        data=self.df, 
                                        eval_env=1, 
                                        return_type= 'dataframe')
            
            self.covariate_names = c.columns.tolist()
        
        if self.hdfe:
            algo = pyhdfe.create(self.df.index.to_frame().values)
            if not isinstance(c, str):
                c = pd.DataFrame(data = algo.residualize(c),
                                            index = c.index,
                                            columns = c.columns)
        else:
            if self.old_entity_effects:
                c = c - c.groupby(level=0).transform('mean')
                
            if self.entity_effects:
                
                c_e_mean = c.groupby(level=0).transform('mean')
                
            else: 
                c_e_mean = 0
                
            if self.time_effects and self.twoway_fixed_effects == 'demean':
                
                c_t_mean = c.groupby(level=1).transform('mean')
            else: 
                c_t_mean = 0
                
            if self.overall_demean:
                overall_c_mean = c.groupby(level=[0,1]).transform('mean')
            else:
                overall_c_mean = 0
            
            if not isinstance(c, str):
                c = c - c_e_mean - c_t_mean + overall_c_mean
        
        return c.values
    
    @functools.cached_property
    def X(self):
        return self.regime_list[:,:, 1:]
    
    @functools.cached_property
    def y(self):
        return self.regime_list[:,:,0]
    
    @functools.cached_property
    def ind(self):
        return self.df[self.classifier_ind].values
    
    @functools.cached_property
    def p(self):
        return self.df[self.classifier_pred].values
        
    def _drop_singletons(self, data):
        
        driver_time_count = (
            data
            .groupby(level=0)[data.columns[0]] # Just getting some column
            .count()
            )
        
        singleton_drivers = driver_time_count[np.where(driver_time_count == 1)[0]].index
        
        return data.loc[lambda df: df.index.get_level_values(0).difference(singleton_drivers)]
        
    @property
    def exog_names(self):
        return self.data.xnames

    @exog_names.setter
    def exog_names(self, names):
        self.data.xnames = names
        

    def _ll(self, sigma_vec, beta_mat, beta_c_mat):
                
        
        if self.n_regimes == 4:
            cm = np.array(
                [
                    [0.85400498, 0.17394031, 0.0470923, 0.17593651],
                    [0.07902572, 0.71988785, 0.13576904, 0.04206538],
                    [0.00444184, 0.05345483, 0.7683022, 0.01397825],
                    [0.06252746, 0.05271701, 0.04883646, 0.76801986],
                ]
            )

        elif self.n_regimes == 10:
            cm = np.array(
                [
                    [
                        7.51733523e-01,
                        3.36037080e-02,
                        1.06639147e-02,
                        1.33630290e-02,
                        9.74529347e-02,
                        7.45621493e-02,
                        5.60966108e-03,
                        2.33992767e-03,
                        2.18987342e-02,
                        5.46599963e-03,
                    ],
                    [
                        1.19240490e-02,
                        8.86442642e-01,
                        1.71998624e-03,
                        5.93912398e-04,
                        1.60149928e-02,
                        1.70039109e-03,
                        3.11647838e-04,
                        0.00000000e00,
                        2.53164557e-03,
                        2.77932185e-04,
                    ],
                    [
                        1.15352213e-02,
                        4.05561993e-03,
                        5.24251806e-01,
                        2.87552586e-02,
                        2.17224636e-02,
                        1.30079918e-02,
                        4.37086093e-02,
                        7.53031270e-02,
                        8.17721519e-02,
                        1.17750602e-01,
                    ],
                    [
                        8.73566198e-02,
                        1.62224797e-02,
                        1.24183007e-01,
                        7.07745608e-01,
                        3.45003833e-02,
                        1.86958000e-01,
                        1.97506817e-01,
                        1.21676239e-01,
                        6.70886076e-02,
                        1.13118399e-01,
                    ],
                    [
                        2.98749271e-02,
                        3.36037080e-02,
                        5.84795322e-03,
                        1.68275179e-03,
                        7.81412386e-01,
                        3.65584084e-03,
                        1.63615115e-03,
                        1.27632419e-03,
                        2.83544304e-02,
                        2.03816935e-03,
                    ],
                    [
                        8.38571706e-02,
                        1.50637312e-02,
                        2.20158239e-02,
                        4.91957436e-02,
                        1.95928103e-02,
                        6.75990478e-01,
                        1.19984418e-02,
                        3.40353116e-03,
                        1.75949367e-02,
                        1.29701686e-02,
                    ],
                    [
                        5.05475990e-03,
                        4.05561993e-03,
                        5.02235982e-02,
                        1.68225687e-01,
                        1.44816424e-03,
                        2.27852406e-02,
                        4.15894040e-01,
                        1.66985748e-01,
                        3.79746835e-03,
                        1.37669075e-01,
                    ],
                    [
                        1.68491997e-03,
                        0.00000000e00,
                        1.61678707e-02,
                        7.72086117e-03,
                        1.70372263e-04,
                        3.48580173e-03,
                        1.18426178e-01,
                        4.69049138e-01,
                        1.64556962e-03,
                        6.95756902e-02,
                    ],
                    [
                        1.09519798e-02,
                        5.79374276e-03,
                        2.23598211e-02,
                        3.46448899e-03,
                        2.53002811e-02,
                        3.74086040e-03,
                        1.16867939e-03,
                        2.12720698e-04,
                        7.68481013e-01,
                        4.53955901e-03,
                    ],
                    [
                        6.02682911e-03,
                        1.15874855e-03,
                        2.22566219e-01,
                        1.92526602e-02,
                        2.38521169e-03,
                        1.41132460e-02,
                        2.03739774e-01,
                        1.59753244e-01,
                        6.83544304e-03,
                        5.36594404e-01,
                    ],
                ]
            )
            
        if isinstance(self.covariates, str):
            loc = self.X@beta_mat[0,:]
        else:
            loc = self.X@beta_mat[0,:] + self.covariates@beta_c_mat[0]

        rnl = norm.pdf(self.y, loc, scale=np.abs(sigma_vec[0])).T
    
        return np.log((rnl*((self.ind*self.p)@cm.T)).sum(axis=1))

    def _params_to_ll(self, params):

        # Since we always put the covariates at the end, take them out from the end
        # regime_params = res.params.values[:-num_covariates]        
        
        if self.same_impact:
            beta_mat = np.tile(params[0:self.num_regime_vars], self.n_regimes).reshape(self.n_regimes, self.num_regime_vars)
        else:
            beta_mat = params[0 : -(self.num_covariates + 1)].reshape(self.n_regimes, self.num_regime_vars)
        
        beta_c_mat = np.tile(params[-(self.num_covariates +1):-1], self.n_regimes).reshape(self.n_regimes,self.num_covariates)
        sigma_vec = np.repeat(params[-1], self.n_regimes) # sigma is always last
            
        return beta_mat, beta_c_mat, sigma_vec

    def nloglikeobs(self, params):
        """Negative log-likelihood for an observation. The params matrix is the strange thing here
        and needs to be better defined.

        Args:
            params (ndarray): The matrix of parameters to optimize

        """

        beta_mat, beta_c_mat, sigma_vec = self._params_to_ll(params)

        ll = self._ll(
            beta_mat=beta_mat, beta_c_mat= beta_c_mat, sigma_vec=sigma_vec,
        )

        return -ll

    def apply_exog_names(self, regime_impact_names =None):
        
        if self.same_impact:
            regime_effects = regime_impact_names
        else:
            regime_effects = reduce(lambda x, y: x+ y, [i[1].columns.tolist() for i in self.regime_list])
        covariate_effects = self.covariate_names

        sigmas = ["sigma"]

        self.exog_names = regime_effects + covariate_effects + sigmas

    def bounds(self, sigma_bound):
        

        # Now set up bounds on variables
        if self.same_impact:
            beta_bounds = [(None, None) for i in range(self.num_regime_vars + self.num_covariates)]
        else:
            beta_bounds = [(None, None) for i in range(self.n_regimes * self.num_regime_vars +  self.num_covariates)]
        
        sigma_bounds = [sigma_bound]

        bounds = tuple(beta_bounds + sigma_bounds)

        return bounds
    
    def _start_params(self, show_ols = False):
        """Runs OLS regression to get start params for MLE coefficients
        """
        
        # Create formula for running regression
        
        if self.entity_effects:
            regimes = [' + '.join(d[1].columns.tolist()) for d in self.regime_list]

            interacted_formula = [f"{r}:({i})" for r,i in zip(self.classifier_ind, regimes)]
        else:
            regimes = [' + '.join(d[1].columns.drop('Intercept').tolist()) for d in self.regime_list]

            interacted_formula = [f"{r} + {r}:({i})" for r,i in zip(self.classifier_ind, regimes)]

        ols_formula = self.regime_list[0][0].columns.tolist()[0] \
            + " ~ " + ' + '.join(interacted_formula) + " + " \
                + ' + '.join(self.covariates.columns.tolist()) + "-1 "
                
        
                
        print("Creating starting values...")
        if self.entity_effects:
            mod = PanelOLS.from_formula(ols_formula + ' + EntityEffects', 
                                        data=self.df, 
                                        drop_absorbed=True)
            res = mod.fit()
            summary = res.summary
        else:
            mod = smf.ols(ols_formula, data=self.df)
            res = mod.fit()
            summary = res.summary()
        
        # Now get sigma
        sigma = self.df[self.regime_list[0][0].columns.tolist()[0]].std()

        if show_ols:
            return print(summary)
        
        y, X = dmatrices(ols_formula, data=self.df, return_type='dataframe')
        
        if np.linalg.matrix_rank(X) != X.shape[1]:
            raise Exception("Exogenous variables is not full rank.")            
        
        return np.append(res.params.values, sigma)
    
    def fit(
        self,
        method=None,
        start_params=None,
        maxiter=10000,
        maxfun=5000,
        sigma_bound=None,
        regime_impact_names = None,
        **kwds,
    ):

        self.apply_exog_names(regime_impact_names=regime_impact_names)


        if start_params is None:
            start_params = self._start_params(show_ols=False)
            
        if self.time_effects and self.twoway_fixed_effects=='dummy':
            # get dummies for time variable
            
            # regress outcome on dummies to get start_params
            res_dummies = (
                sm.OLS(self.regime_list[0][0].values, 
                       self.covariates.values)
                .fit()
                .params[self.num_covariates:]
                )

            start_params = np.append(np.append(start_params[:-1], res_dummies), start_params[-1])
        
        if kwds.get('cov_type') is None:
            cov_type='cluster'
            cov_kwds = {'groups' : self.df.gaul_class,
                        'df_correction' : True,
                        'use_correction' : True}
        else:
            cov_type = kwds.pop('cov_type', None)
            cov_kwds = kwds.pop('cov_kwds', None) 

         
        optimize = super().fit(
            method=method,
            start_params=start_params,
            maxiter=maxiter,
            maxfun=maxfun,
            eps=1e-08,
            ftol=1e-10,
            bounds=self.bounds(sigma_bound=sigma_bound),
            cov_type= cov_type,
            cov_kwds = cov_kwds,
            use_t=True,
            **kwds
        )
        # self._start_params(show_ols=show_ols)

        return optimize



