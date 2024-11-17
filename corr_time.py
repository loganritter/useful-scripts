import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
import pandas as pd

def read_gcmc_data(filename):
    """
    Read GCMC simulation data from a text file.
    
    Parameters:
    -----------
    filename : str
        Path to the text file containing GCMC data
        
    Returns:
    --------
    dict
        Dictionary containing the data arrays
    """
    try:
        data = pd.read_csv(filename, 
                          sep=r'\s+',
                          header=None,
                          names=['steps', 'uptake', 'n_particles', 'potential'])
        
        # Convert to dictionary of numpy arrays
        data_dict = {
            'steps': data['steps'].values,
            'uptake': data['uptake'].values,
            'n_particles': data['n_particles'].values,
            'potential': data['potential'].values
        }
        
        return data_dict
    
    except Exception as e:
        print(f"Error reading file {filename}: {str(e)}")
        raise

def autocorrelation(data, maxlag=None):
    """
    Calculate the autocorrelation function for a time series.
    
    Parameters:
    -----------
    data : array-like
        Time series data
    maxlag : int, optional
        Maximum lag time to calculate correlation. Default is N//2
        
    Returns:
    --------
    lags : array
        Lag times
    acf : array
        Autocorrelation function values
    """
    N = len(data)
    if maxlag is None:
        maxlag = N // 2
    
    # Normalize the data
    data = np.array(data)
    data = data - np.mean(data)
    data = data / np.std(data)
    
    # Calculate autocorrelation
    acf = np.correlate(data, data, mode='full')
    acf = acf[N-1:] # Keep only the positive lags
    acf = acf[:maxlag] # Trim to maxlag
    
    # Normalize
    acf = acf / N
    
    lags = np.arange(len(acf))
    return lags, acf

def calculate_correlation_time(acf, lags):
    """
    Calculate the correlation time by integrating the ACF until it first crosses zero
    or reaches 1/e of its initial value.
    
    Parameters:
    -----------
    acf : array
        Autocorrelation function values
    lags : array
        Lag times
        
    Returns:
    --------
    tau : float
        Correlation time
    """
    # Find where ACF crosses 1/e
    threshold = 1/np.e
    try:
        # Find first crossing of 1/e
        idx = np.where(acf < threshold)[0][0]
        tau = np.trapz(acf[:idx], lags[:idx])
    except IndexError:
        # If ACF never crosses 1/e, use all available data
        tau = np.trapz(acf, lags)
    
    return tau

def analyze_gcmc_equilibration(filename, maxlag=None):
    """
    Read GCMC data from file and analyze equilibration by calculating autocorrelation
    functions and correlation times, and check if the system has reached equilibrium.
    
    Parameters:
    -----------
    filename : str
        Path to the text file containing GCMC data
    maxlag : int, optional
        Maximum lag time for autocorrelation calculation
        
    Returns:
    --------
    dict
        Dictionary containing analysis results
    """
    print(f"\nAnalyzing file: {filename}")
    print("=" * 50)
    
    # Read the data
    data = read_gcmc_data(filename)
    
    # Calculate time step from steps column
    time_step = np.mean(np.diff(data['steps']))
    
    # Calculate ACFs for all relevant quantities
    lags_u, acf_u = autocorrelation(data['uptake'], maxlag)
    lags_n, acf_n = autocorrelation(data['n_particles'], maxlag)
    lags_p, acf_p = autocorrelation(data['potential'], maxlag)
    
    # Scale lags by time_step
    lags_u = lags_u * time_step
    lags_n = lags_n * time_step
    lags_p = lags_p * time_step
    
    # Calculate correlation times
    tau_u = calculate_correlation_time(acf_u, lags_u)
    tau_n = calculate_correlation_time(acf_n, lags_n)
    tau_p = calculate_correlation_time(acf_p, lags_p)
    
    # Check if ACF decays to 1/e within a reasonable time
    def equilibrium_check(acf, lags):
        threshold = 1/np.e
        try:
            idx = np.where(acf < threshold)[0][0]
            return "Yes" if lags[idx] <= 0.2 * lags[-1] else "No"
        except IndexError:
            return "No"

    equil_u = equilibrium_check(acf_u, lags_u)
    equil_n = equilibrium_check(acf_n, lags_n)
    equil_p = equilibrium_check(acf_p, lags_p)

    # Print correlation times and equilibration status
    print("\nCorrelation Times and Equilibration Check:")
    print("-" * 50)
    print(f"Uptake:          τ = {tau_u:10.2f} steps | Equilibrium reached: {equil_u}")
    print(f"N particles:     τ = {tau_n:10.2f} steps | Equilibrium reached: {equil_n}")
    print(f"Potential:       τ = {tau_p:10.2f} steps | Equilibrium reached: {equil_p}")
    
    # Create plots
    fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(10, 12))
    fig_raw, (ax_r1, ax_r2, ax_r3) = plt.subplots(3, 1, figsize=(10, 12))
    
    # Uptake plots
    ax1.plot(lags_u, acf_u, 'b-', label=f'τ = {tau_u:.1f} steps')
    ax1.axhline(y=1/np.e, color='r', linestyle='--', alpha=0.5)
    ax1.set_xlabel('Lag time (steps)')
    ax1.set_ylabel('Uptake ACF')
    ax1.legend()
    ax1.grid(True)
    
    ax_r1.plot(data['steps'], data['uptake'], 'b-')
    ax_r1.set_xlabel('Steps')
    ax_r1.set_ylabel('Uptake (mmol/g)')
    ax_r1.grid(True)
    
    # Number of particles plots
    ax2.plot(lags_n, acf_n, 'g-', label=f'τ = {tau_n:.1f} steps')
    ax2.axhline(y=1/np.e, color='r', linestyle='--', alpha=0.5)
    ax2.set_xlabel('Lag time (steps)')
    ax2.set_ylabel('N particles ACF')
    ax2.legend()
    ax2.grid(True)
    
    ax_r2.plot(data['steps'], data['n_particles'], 'g-')
    ax_r2.set_xlabel('Steps')
    ax_r2.set_ylabel('Number of particles')
    ax_r2.grid(True)
    
    # Potential energy plots
    ax3.plot(lags_p, acf_p, 'r-', label=f'τ = {tau_p:.1f} steps')
    ax3.axhline(y=1/np.e, color='r', linestyle='--', alpha=0.5)
    ax3.set_xlabel('Lag time (steps)')
    ax3.set_ylabel('Potential Energy ACF')
    ax3.legend()
    ax3.grid(True)
    
    ax_r3.plot(data['steps'], data['potential'], 'r-')
    ax_r3.set_xlabel('Steps')
    ax_r3.set_ylabel('Potential Energy')
    ax_r3.grid(True)
    
    plt.tight_layout()
    
    # Calculate basic statistics
    stats_dict = {
        'uptake_mean': np.mean(data['uptake']),
        'uptake_std': np.std(data['uptake']),
        'n_particles_mean': np.mean(data['n_particles']),
        'n_particles_std': np.std(data['n_particles']),
        'potential_mean': np.mean(data['potential']),
        'potential_std': np.std(data['potential'])
    }
    
    # Print statistics
    print("\nBasic Statistics:")
    print("-" * 30)
    print(f"Uptake:      {stats_dict['uptake_mean']:10.2f} ± {stats_dict['uptake_std']:6.2f} mmol/g")
    print(f"N particles: {stats_dict['n_particles_mean']:10.2f} ± {stats_dict['n_particles_std']:6.2f}")
    print(f"Potential:   {stats_dict['potential_mean']:10.2f} ± {stats_dict['potential_std']:6.2f}")
    print("\n")
    
    results = {
        'uptake_correlation_time': tau_u,
        'nparticles_correlation_time': tau_n,
        'potential_correlation_time': tau_p,
        'lags_uptake': lags_u,
        'acf_uptake': acf_u,
        'lags_n': lags_n,
        'acf_n': acf_n,
        'lags_potential': lags_p,
        'acf_potential': acf_p,
        'statistics': stats_dict,
        'acf_figure': fig,
        'raw_data_figure': fig_raw,
        'equilibration_check': {
            'uptake': equil_u,
            'n_particles': equil_n,
            'potential': equil_p
        }
    }
    
    return results

if __name__ == "__main__":
    filename = "data.txt"  # Replace with your actual filename
    
    try:
        results = analyze_gcmc_equilibration(filename)
        plt.show()
        
    except Exception as e:
        print(f"Error during analysis: {str(e)}")
