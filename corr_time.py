import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
import pandas as pd
import sys
import argparse

class GCMCStatistics:
    """
    A class for analyzing Grand Canonical Monte Carlo (GCMC) simulation data.
    
    Attributes:
    -----------
    filename : str
        Path to the GCMC data file
    data : dict
        Dictionary containing the loaded data arrays
    results : dict
        Dictionary containing analysis results
    maxlag : int, optional
        Maximum lag time for correlation calculations
    """
    
    def __init__(self, filename, maxlag=None):
        """
        Initialize the GCMCStatistics with a data file.
        
        Parameters:
        -----------
        filename : str
            Path to the GCMC data file
        maxlag : int, optional
            Maximum lag time for correlation calculations
        """
        self.filename = filename
        self.maxlag = maxlag
        self.data = None
        self.results = {}
        self.time_step = None
        
    def read_data(self):
        try:
            data = pd.read_csv(self.filename, 
                             sep=r'\s+',
                             header=None,
                             names=['steps', 'uptake', 'n_particles', 'potential'])
            
            self.data = {
                'steps': data['steps'].values,
                'uptake': data['uptake'].values,
                'n_particles': data['n_particles'].values,
                'potential': data['potential'].values
            }
            
            self.time_step = np.mean(np.diff(self.data['steps']))
            
        except Exception as e:
            print(f"Error reading file {self.filename}: {str(e)}")
            raise
            
    def calculate_autocorrelation(self, data):
        """
        Calculate autocorrelation function for a time series.
        
        Parameters:
        -----------
        data : array-like
            Time series data
            
        Returns:
        --------
        tuple
            (lags, acf) arrays
        """
        N = len(data)
        maxlag = self.maxlag if self.maxlag is not None else N // 2
        
        # Normalize the data
        data = np.array(data)
        data = (data - np.mean(data)) / np.std(data)

        # Calculate autocorrelation
        acf = np.correlate(data, data, mode='full')[N-1:]
        acf = acf[:maxlag] / N
        lags = np.arange(len(acf))
        
        return lags, acf
        
    def calculate_correlation_time(self, acf, lags):
        """
        Calculate correlation time from ACF.
        
        Parameters:
        -----------
        acf : array
            Autocorrelation function values
        lags : array
            Lag times
            
        Returns:
        --------
        float
            Correlation time
        """
        threshold = 1/np.e
        try:
            idx = np.where(acf < threshold)[0][0]
            tau = np.trapz(acf[:idx], lags[:idx])
        except IndexError:
            tau = np.trapz(acf, lags)
        
        return tau
        
    def check_equilibration(self, acf, lags):
        """
        Check if system has reached equilibrium.
        
        Parameters:
        -----------
        acf : array
            Autocorrelation function values
        lags : array
            Lag times
            
        Returns:
        --------
        str
            'Yes' or 'No' indicating equilibration status
        """
        threshold = 1/np.e
        try:
            idx = np.where(acf < threshold)[0][0]
            return "Yes" if lags[idx] <= 0.2 * lags[-1] else "No"
        except IndexError:
            return "No"
            
    def calculate_statistics(self):
        self.results['statistics'] = {
            'uptake_mean': np.mean(self.data['uptake']),
            'uptake_std': np.std(self.data['uptake']),
            'n_particles_mean': np.mean(self.data['n_particles']),
            'n_particles_std': np.std(self.data['n_particles']),
            'potential_mean': np.mean(self.data['potential']),
            'potential_std': np.std(self.data['potential'])
        }
        
    def create_plots(self):
        # Create figure for ACFs
        fig_acf, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(10, 12))
        
        # Create figure for raw data
        fig_raw, (ax_r1, ax_r2, ax_r3) = plt.subplots(3, 1, figsize=(10, 12))
        
        # Plot ACFs
        variables = ['uptake', 'n_particles', 'potential']
        colors = ['b', 'g', 'r']
        axes_acf = [ax1, ax2, ax3]
        axes_raw = [ax_r1, ax_r2, ax_r3]
        labels = ['Uptake', 'N particles', 'Potential Energy']
        
        for var, color, ax_acf, ax_raw, label in zip(variables, colors, axes_acf, axes_raw, labels):
            # Get correlation data
            lags = self.results[f'{var}_lags']
            acf = self.results[f'{var}_acf']
            tau = self.results[f'{var}_correlation_time']
            
            # Plot ACF
            ax_acf.plot(lags, acf, f'{color}-', label=f'τ = {tau:.1f} steps')
            ax_acf.axhline(y=1/np.e, color='r', linestyle='--', alpha=0.5)
            ax_acf.set_xlabel('Lag time (steps)')
            ax_acf.set_ylabel(f'{label} ACF')
            ax_acf.legend()
            ax_acf.grid(True)
            
            # Plot raw data
            ax_raw.plot(self.data['steps'], self.data[var], f'{color}-')
            ax_raw.set_xlabel('Steps')
            ax_raw.set_ylabel(label)
            ax_raw.grid(True)
            
        plt.tight_layout()
        
        # Save figures
        fig_acf.savefig('acf_plots.png')
        fig_raw.savefig('raw_data_plots.png')
        
        self.results['figures'] = {
            'acf': fig_acf,
            'raw': fig_raw
        }
        
    def print_results(self):
        print(f"\nAnalyzing file: {self.filename}")
        print("=" * 50)
        
        # Print correlation times and equilibration status
        print("\nCorrelation Times and Equilibration Check:")
        print("-" * 50)
        for var in ['uptake', 'n_particles', 'potential']:
            tau = self.results[f'{var}_correlation_time']
            equil = self.results['equilibration_check'][var]
            print(f"{var:15} τ = {tau:10.2f} steps | Equilibrium reached: {equil}")
        
        # Print statistics
        stats = self.results['statistics']
        print("\nBasic Statistics:")
        print("-" * 30)
        print(f"Uptake:      {stats['uptake_mean']:10.2f} ± {stats['uptake_std']:6.2f} mmol/g")
        print(f"N particles: {stats['n_particles_mean']:10.2f} ± {stats['n_particles_std']:6.2f}")
        print(f"Potential:   {stats['potential_mean']:10.2f} ± {stats['potential_std']:6.2f}")
        print("\nPlots saved as 'acf_plots.png' and 'raw_data_plots.png'")
        
    def analyze(self):
        self.read_data()
        
        # Analyze each variable
        for var in ['uptake', 'n_particles', 'potential']:
            # Calculate ACF
            lags, acf = self.calculate_autocorrelation(self.data[var])
            scaled_lags = lags * self.time_step
            
            # Store results
            self.results[f'{var}_lags'] = scaled_lags
            self.results[f'{var}_acf'] = acf
            self.results[f'{var}_correlation_time'] = self.calculate_correlation_time(acf, scaled_lags)
            
        # Check equilibration
        self.results['equilibration_check'] = {
            var: self.check_equilibration(self.results[f'{var}_acf'], 
                                        self.results[f'{var}_lags'])
            for var in ['uptake', 'n_particles', 'potential']
        }
        
        self.calculate_statistics()
        self.create_plots()
        self.print_results()
        
        return self.results

def main():
    parser = argparse.ArgumentParser(description='Analyze GCMC simulation data for correlation times and equilibration.')
    parser.add_argument('filename', type=str, help='Path to the GCMC data file')
    parser.add_argument('--maxlag', type=int, help='Maximum lag time for correlation calculation', default=None)
    args = parser.parse_args()
    
    try:
        analyzer = GCMCStatistics(args.filename, args.maxlag)
        results = analyzer.analyze()
        plt.show()
    except Exception as e:
        print(f"Error during analysis: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
