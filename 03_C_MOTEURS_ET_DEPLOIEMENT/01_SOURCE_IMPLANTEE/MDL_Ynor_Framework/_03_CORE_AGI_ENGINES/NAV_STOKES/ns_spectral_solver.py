import numpy as np
import scipy.fft as fft
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import json
import time

class NavierStokes3DSpectral:
    """
    Pseudo-spectral solver for 3D Incompressible Navier-Stokes 
    on a periodic torus [0, 2pi]^3.
    Uses 2/3 de-aliasing and a semi-implicit time stepping 
    (Adams-Bashforth 2 for non-linear, Crank-Nicolson for diffusion).
    """
    def __init__(self, N=64, nu=0.01, dt=0.001, T_final=1.0):
        self.N = N
        self.nu = nu
        self.dt = dt
        self.T_final = T_final
        
        # Grid setup
        self.L = 2.0 * np.pi
        self.dx = self.L / N
        self.x = np.linspace(0, self.L, N, endpoint=False)
        self.X, self.Y, self.Z = np.meshgrid(self.x, self.x, self.x, indexing='ij')
        
        # Wavenumbers
        k = np.fft.fftfreq(N) * N
        self.kx, self.ky, self.kz = np.meshgrid(k, k, k, indexing='ij')
        self.k2 = self.kx**2 + self.ky**2 + self.kz**2
        self.k2[0,0,0] = 1e-12 # avoid division by zero
        
        # Projector to divergence-free space: I - k(k^T)/|k|^2
        self.inv_k2 = 1.0 / self.k2
        self.inv_k2[0,0,0] = 0.0
        
        # Initial condition: Taylor-Green Vortex
        self.u = np.sin(self.X) * np.cos(self.Y) * np.cos(self.Z)
        self.v = -np.cos(self.X) * np.sin(self.Y) * np.cos(self.Z)
        self.w = np.zeros_like(self.X)
        
        # Fourier transforms
        self.u_hat = fft.fftn(self.u)
        self.v_hat = fft.fftn(self.v)
        self.w_hat = fft.fftn(self.w)
        
        # Variables for AB2
        self.Nu_prev = None
        self.Nv_prev = None
        self.Nw_prev = None
        
        self.time = 0.0
        self.history = {'t': [], 'energy': [], 'enstrophy': [], 'mu_margin': []}

    def dealias(self, q_hat):
        """Standard 2/3 rule for de-aliasing."""
        cutoff = self.N / 3.0
        mask = (np.abs(self.kx) < cutoff) & (np.abs(self.ky) < cutoff) & (np.abs(self.kz) < cutoff)
        return q_hat * mask

    def get_nonlinear_term(self, u_hat, v_hat, w_hat):
        # Physical space
        u = fft.ifftn(u_hat).real
        v = fft.ifftn(v_hat).real
        w = fft.ifftn(w_hat).real
        
        # Gradients in Fourier
        ux_hat = 1j * self.kx * u_hat
        uy_hat = 1j * self.ky * u_hat
        uz_hat = 1j * self.kz * u_hat
        
        vx_hat = 1j * self.kx * v_hat
        vy_hat = 1j * self.ky * v_hat
        vz_hat = 1j * self.kz * v_hat
        
        wx_hat = 1j * self.kx * w_hat
        wy_hat = 1j * self.ky * w_hat
        wz_hat = 1j * self.kz * w_hat
        
        # Convection terms in physical space
        conv_u = u * fft.ifftn(ux_hat).real + v * fft.ifftn(uy_hat).real + w * fft.ifftn(uz_hat).real
        conv_v = u * fft.ifftn(vx_hat).real + v * fft.ifftn(vy_hat).real + w * fft.ifftn(vz_hat).real
        conv_w = u * fft.ifftn(wx_hat).real + v * fft.ifftn(wy_hat).real + w * fft.ifftn(wz_hat).real
        
        # Back to Fourier
        conv_u_hat = self.dealias(fft.fftn(conv_u))
        conv_v_hat = self.dealias(fft.fftn(conv_v))
        conv_w_hat = self.dealias(fft.fftn(conv_w))
        
        # Projection to divergence-free space (Leray projection)
        # P[f]_i = f_i - k_i (k \cdot f) / |k|^2
        k_dot_f = self.kx * conv_u_hat + self.ky * conv_v_hat + self.kz * conv_w_hat
        
        Nu = -(conv_u_hat - self.kx * k_dot_f * self.inv_k2)
        Nv = -(conv_v_hat - self.ky * k_dot_f * self.inv_k2)
        Nw = -(conv_w_hat - self.kz * k_dot_f * self.inv_k2)
        
        return Nu, Nv, Nw

    def step(self):
        Nu, Nv, Nw = self.get_nonlinear_term(self.u_hat, self.v_hat, self.w_hat)
        
        if self.Nu_prev is None:
            # First step (Euler explicit for nonlinear)
            Nu_ab = Nu
            Nv_ab = Nv
            Nw_ab = Nw
        else:
            # AB2 for nonlinear
            Nu_ab = 1.5 * Nu - 0.5 * self.Nu_prev
            Nv_ab = 1.5 * Nv - 0.5 * self.Nv_prev
            Nw_ab = 1.5 * Nw - 0.5 * self.Nw_prev
            
        # Crank-Nicolson for diffusion: (I - 0.5*dt*nu*Delta) u^{n+1} = (I + 0.5*dt*nu*Delta) u^n + dt*N
        diff_op_lhs = 1.0 + 0.5 * self.dt * self.nu * self.k2
        diff_op_rhs = 1.0 - 0.5 * self.dt * self.nu * self.k2
        
        self.u_hat = (diff_op_rhs * self.u_hat + self.dt * Nu_ab) / diff_op_lhs
        self.v_hat = (diff_op_rhs * self.v_hat + self.dt * Nv_ab) / diff_op_lhs
        self.w_hat = (diff_op_rhs * self.w_hat + self.dt * Nw_ab) / diff_op_lhs
        
        # Enforce divergence free (numerical hygiene)
        k_dot_u = self.kx * self.u_hat + self.ky * self.v_hat + self.kz * self.w_hat
        self.u_hat -= self.kx * k_dot_u * self.inv_k2
        self.v_hat -= self.ky * k_dot_u * self.inv_k2
        self.w_hat -= self.kz * k_dot_u * self.inv_k2
        
        self.Nu_prev, self.Nv_prev, self.Nw_prev = Nu, Nv, Nw
        self.time += self.dt

    def compute_metrics(self):
        # L2 Energy: 0.5 * integral |u|^2 dx
        energy = 0.5 * np.sum(np.abs(self.u_hat)**2 + np.abs(self.v_hat)**2 + np.abs(self.w_hat)**2) / (self.N**6)
        # Enstrophy: 0.5 * integral |omega|^2 dx = 0.5 * integral |k|^2 |u_hat|^2
        enstrophy = 0.5 * np.sum(self.k2 * (np.abs(self.u_hat)**2 + np.abs(self.v_hat)**2 + np.abs(self.w_hat)**2)) / (self.N**6)
        
        # Vorticity supremum for BKM check
        # omega = curl u
        wx_hat = 1j * (self.ky * self.w_hat - self.kz * self.v_hat)
        wy_hat = 1j * (self.kz * self.u_hat - self.kx * self.w_hat)
        wz_hat = 1j * (self.kx * self.v_hat - self.ky * self.u_hat)
        
        omega_mag = np.sqrt(fft.ifftn(wx_hat).real**2 + fft.ifftn(wy_hat).real**2 + fft.ifftn(wz_hat).real**2)
        vort_max = np.max(omega_mag)
        
        return energy, enstrophy, vort_max

    def run(self, verbose=True):
        print(f"Starting simulation N={self.N}, nu={self.nu}, dt={self.dt}...")
        steps = int(self.T_final / self.dt)
        for i in range(steps):
            self.step()
            if i % 10 == 0:
                e, enst, vmax = self.compute_metrics()
                self.history['t'].append(self.time)
                self.history['energy'].append(float(e))
                self.history['enstrophy'].append(float(enst))
                self.history['mu_margin'].append(float(vmax))
                if verbose and i % 100 == 0:
                    print(f"Step {i}/{steps}: t={self.time:.4f}, Energy={e:.6f}, Enstrophy={enst:.6f}, MaxVort={vmax:.6f}")

    def save_results(self, filename="ns_results.json"):
        with open(filename, 'w') as f:
            json.dump(self.history, f)
        print(f"Results saved to {filename}")

if __name__ == "__main__":
    # Small scale simulation for verification
    solver = NavierStokes3DSpectral(N=32, nu=0.01, dt=0.005, T_final=0.2)
    solver.run()
    solver.save_results("ns_spectral_audit.json")
