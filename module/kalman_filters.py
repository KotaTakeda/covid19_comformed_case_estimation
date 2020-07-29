import numpy as np
from numpy.random import multivariate_normal

# Ensemble Kalman Filter 
"""
Parameters


M: callable(x, dt)
  状態遷移関数

H: callable(x)
  観測関数
Q: ndarray(dim, dim)
  モデルの誤差共分散行列, 
R: ndarray(dim, dim)
  観測の誤差共分散行列

N: アンサンブルメンバーの数



x: ndarray(dim)

"""
class EnKalmanFilter:
    def __init__(self, M, H, Q, R, y, x_0, P_0, dim_x=2, dim_y=1, N=10, dt=0.1):
        self.M = M
        self.H = H
        self.Q = Q
        self.R = R
        # self.A = A # 加法的誤差共分散膨張行列
        self.y = y
        self.N = N
        self.dt = dt
        self.dim_x = dim_x # todo : x_0から計算
        self.dim_y = dim_y # todo : yから計算
        self.mean = np.zeros(self.dim_x)
        self.mean_y = np.zeros(self.dim_y)
        self.x = np.zeros(self.dim_x)
        self.x_log = []

        self._initialize(x_0, P_0, N)

  #　初期状態
    def _initialize(self, x_0, P_0, N):
        self.ensemble = np.zeros((self.N, self.dim_x))
        e = multivariate_normal(self.mean, P_0, N)
        for i in range(N):
            self.ensemble[i] = x_0 + e[i]
    
        self.x = np.mean(self.ensemble, axis=0)
    
  # 逐次推定を行う
    def forwardEstimation(self, verbose=True):
        count = 0
        for y_obs in self.y:
            self._update(y_obs)
            self._forecast()

            if verbose:
                if count%10 == 0:
                    print('step: {}, x: {}'.format(count, self.x))
                count += 1

    # 更新/解析
    def _update(self, y_obs):
        N = self.N
        dim_y = self.dim_y

        # アンサンブルで観測，ノイズのせる
        e = multivariate_normal(self.mean_y, self.R, N)
        ensemble_y = np.zeros((N, dim_y))
        for i in range(N):
            ensemble_y[i] = self.H(self.ensemble[i]) + e[i]

        y_mean = np.mean(ensemble_y, axis=0)

        #dx dy
        dX = self.ensemble - self.x
        dY = ensemble_y - y_mean

        # Pxy Pyy
        P_xy = (dX.T@dY) / (N-1)
        P_yy = (dY.T@dY) / (N-1) 

        # Kalman gain 
        K = P_xy@np.linalg.inv(P_yy + self.R)

        # アンサンブルで x(k) 更新
        for i in range(N):
            self.ensemble[i] += K@(y_obs - ensemble_y[i])

        # 更新した値のアンサンブル平均　x を保存
        self.x = np.mean(self.ensemble, axis=0)
        self.x_log.append(self.x)

    # 予報/時間発展
    def _forecast(self, log=False):
    # アンサンブルで x(k) 予測
        for i, s in enumerate(self.ensemble):
            self.ensemble[i] = self.M(s, self.dt)
    
        # 加法的誤差共分散膨張に対応
        # e = multivariate_normal(self.mean, self.A, self.N)
        # e = multivariate_normal(self.mean, self.Q, self.N)
        # self.ensemble += e

        self.x = np.mean(self.ensemble, axis=0)

        if log:
            self.x_log.append(self.x)
    
    # 追加の推定(観測値なし)
    def additional_forecast(self, step):
        for _ in range(step):
            self._forecast(log=True)