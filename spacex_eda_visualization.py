"""
SpaceX Falcon 9 First Stage Landing Prediction
Part 2: Exploratory Data Analysis with Visualization

This script performs comprehensive EDA on SpaceX launch data
using matplotlib and seaborn for visualization.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# Set style for better-looking plots
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 6)

class SpaceXEDA:
    """Class for Exploratory Data Analysis of SpaceX launch data"""
    
    def __init__(self, data_path='data/spacex_launch_data.csv'):
        """Initialize with data path"""
        self.data_path = data_path
        self.df = None
        
    def load_data(self):
        """Load data from CSV"""
        self.df = pd.read_csv(self.data_path)
        self.df['Date'] = pd.to_datetime(self.df['Date'])
        print(f"Data loaded: {self.df.shape[0]} rows, {self.df.shape[1]} columns")
        return self.df
    
    def basic_statistics(self):
        """Display basic statistical information"""
        print("\n" + "="*60)
        print("BASIC STATISTICS")
        print("="*60)
        
        print(f"\nTotal Falcon 9 Launches: {len(self.df)}")
        print(f"Successful Landings: {self.df['Class'].sum()}")
        print(f"Failed Landings: {len(self.df) - self.df['Class'].sum()}")
        print(f"Success Rate: {self.df['Class'].mean()*100:.2f}%")
        
        print(f"\nDate Range: {self.df['Date'].min()} to {self.df['Date'].max()}")
        print(f"\nUnique Launch Sites: {self.df['LaunchSite'].nunique()}")
        print(f"Unique Orbits: {self.df['Orbit'].nunique()}")
        
        if 'PayloadMass' in self.df.columns:
            payload_data = self.df[self.df['PayloadMass'] > 0]['PayloadMass']
            if len(payload_data) > 0:
                print(f"\nPayload Mass Statistics:")
                print(f"  Average: {payload_data.mean():.2f} kg")
                print(f"  Min: {payload_data.min():.2f} kg")
                print(f"  Max: {payload_data.max():.2f} kg")
    
    def plot_success_rate_over_time(self):
        """Plot landing success rate over time"""
        df_time = self.df.copy()
        df_time['Year'] = df_time['Date'].dt.year
        
        # Calculate success rate by year
        success_by_year = df_time.groupby('Year')['Class'].agg(['sum', 'count', 'mean'])
        success_by_year['success_rate'] = success_by_year['mean'] * 100
        
        plt.figure(figsize=(12, 6))
        plt.subplot(1, 2, 1)
        plt.plot(success_by_year.index, success_by_year['success_rate'], marker='o', linewidth=2)
        plt.xlabel('Year', fontsize=12)
        plt.ylabel('Success Rate (%)', fontsize=12)
        plt.title('First Stage Landing Success Rate Over Time', fontsize=14, fontweight='bold')
        plt.grid(True, alpha=0.3)
        
        plt.subplot(1, 2, 2)
        plt.bar(success_by_year.index, success_by_year['count'], alpha=0.7, color='steelblue')
        plt.xlabel('Year', fontsize=12)
        plt.ylabel('Number of Launches', fontsize=12)
        plt.title('Number of Falcon 9 Launches per Year', fontsize=14, fontweight='bold')
        plt.grid(True, alpha=0.3, axis='y')
        
        plt.tight_layout()
        plt.savefig('images/success_rate_over_time.png', dpi=300, bbox_inches='tight')
        print("✓ Saved: images/success_rate_over_time.png")
        plt.close()
    
    def plot_success_by_launch_site(self):
        """Plot success rate by launch site"""
        site_success = self.df.groupby('LaunchSite')['Class'].agg(['sum', 'count', 'mean'])
        site_success['success_rate'] = site_success['mean'] * 100
        site_success = site_success.sort_values('success_rate', ascending=False)
        
        plt.figure(figsize=(12, 6))
        plt.subplot(1, 2, 1)
        plt.barh(range(len(site_success)), site_success['success_rate'], color='green', alpha=0.7)
        plt.yticks(range(len(site_success)), site_success.index)
        plt.xlabel('Success Rate (%)', fontsize=12)
        plt.title('Landing Success Rate by Launch Site', fontsize=14, fontweight='bold')
        plt.grid(True, alpha=0.3, axis='x')
        
        plt.subplot(1, 2, 2)
        plt.barh(range(len(site_success)), site_success['count'], color='steelblue', alpha=0.7)
        plt.yticks(range(len(site_success)), site_success.index)
        plt.xlabel('Number of Launches', fontsize=12)
        plt.title('Number of Launches by Site', fontsize=14, fontweight='bold')
        plt.grid(True, alpha=0.3, axis='x')
        
        plt.tight_layout()
        plt.savefig('images/success_by_launch_site.png', dpi=300, bbox_inches='tight')
        print("✓ Saved: images/success_by_launch_site.png")
        plt.close()
    
    def plot_success_by_orbit(self):
        """Plot success rate by orbit type"""
        orbit_success = self.df.groupby('Orbit')['Class'].agg(['sum', 'count', 'mean'])
        orbit_success['success_rate'] = orbit_success['mean'] * 100
        orbit_success = orbit_success[orbit_success['count'] >= 5]  # Filter orbits with at least 5 launches
        orbit_success = orbit_success.sort_values('success_rate', ascending=False)
        
        plt.figure(figsize=(14, 6))
        x = range(len(orbit_success))
        plt.bar(x, orbit_success['success_rate'], alpha=0.7, color='coral')
        plt.xticks(x, orbit_success.index, rotation=45, ha='right')
        plt.xlabel('Orbit Type', fontsize=12)
        plt.ylabel('Success Rate (%)', fontsize=12)
        plt.title('Landing Success Rate by Orbit Type (min 5 launches)', fontsize=14, fontweight='bold')
        plt.grid(True, alpha=0.3, axis='y')
        plt.tight_layout()
        plt.savefig('images/success_by_orbit.png', dpi=300, bbox_inches='tight')
        print("✓ Saved: images/success_by_orbit.png")
        plt.close()
    
    def plot_payload_vs_success(self):
        """Plot relationship between payload mass and landing success"""
        df_payload = self.df[self.df['PayloadMass'] > 0].copy()
        
        if len(df_payload) > 0:
            plt.figure(figsize=(12, 6))
            
            # Scatter plot
            success_color = df_payload['Class'].map({0: 'red', 1: 'green'})
            plt.scatter(df_payload['PayloadMass'], df_payload.index, 
                       c=success_color, alpha=0.6, s=50)
            plt.xlabel('Payload Mass (kg)', fontsize=12)
            plt.ylabel('Launch Index', fontsize=12)
            plt.title('Payload Mass vs Landing Success', fontsize=14, fontweight='bold')
            plt.legend(['Failed', 'Success'])
            plt.grid(True, alpha=0.3)
            
            plt.tight_layout()
            plt.savefig('images/payload_vs_success.png', dpi=300, bbox_inches='tight')
            print("✓ Saved: images/payload_vs_success.png")
            plt.close()
    
    def plot_correlation_heatmap(self):
        """Plot correlation heatmap of numerical features"""
        numerical_features = ['FlightNumber', 'PayloadCount', 'PayloadMass', 'GridFins', 
                            'Reused', 'Legs', 'Class']
        
        # Filter columns that exist in the dataframe
        available_features = [col for col in numerical_features if col in self.df.columns]
        df_numerical = self.df[available_features].copy()
        
        # Convert boolean to int
        for col in df_numerical.columns:
            if df_numerical[col].dtype == 'bool':
                df_numerical[col] = df_numerical[col].astype(int)
        
        # Calculate correlation
        correlation = df_numerical.corr()
        
        plt.figure(figsize=(10, 8))
        sns.heatmap(correlation, annot=True, fmt='.2f', cmap='coolwarm', center=0,
                   square=True, linewidths=1, cbar_kws={"shrink": 0.8})
        plt.title('Feature Correlation Heatmap', fontsize=14, fontweight='bold')
        plt.tight_layout()
        plt.savefig('images/correlation_heatmap.png', dpi=300, bbox_inches='tight')
        print("✓ Saved: images/correlation_heatmap.png")
        plt.close()
    
    def plot_feature_importance(self):
        """Plot feature importance for landing success"""
        features_to_analyze = ['GridFins', 'Reused', 'Legs']
        
        fig, axes = plt.subplots(1, 3, figsize=(15, 5))
        
        for idx, feature in enumerate(features_to_analyze):
            if feature in self.df.columns:
                success_rate = self.df.groupby(feature)['Class'].mean() * 100
                axes[idx].bar(['No', 'Yes'], success_rate.values, color=['red', 'green'], alpha=0.7)
                axes[idx].set_ylabel('Success Rate (%)', fontsize=11)
                axes[idx].set_title(f'Success Rate by {feature}', fontsize=12, fontweight='bold')
                axes[idx].grid(True, alpha=0.3, axis='y')
                axes[idx].set_ylim([0, 100])
        
        plt.tight_layout()
        plt.savefig('images/feature_importance.png', dpi=300, bbox_inches='tight')
        print("✓ Saved: images/feature_importance.png")
        plt.close()
    
    def generate_summary_report(self):
        """Generate a comprehensive summary report"""
        report = []
        report.append("="*70)
        report.append("SPACEX FALCON 9 - EXPLORATORY DATA ANALYSIS SUMMARY")
        report.append("="*70)
        report.append("")
        
        # Overall statistics
        report.append("1. OVERALL STATISTICS")
        report.append("-" * 70)
        report.append(f"   Total Launches: {len(self.df)}")
        report.append(f"   Successful Landings: {self.df['Class'].sum()}")
        report.append(f"   Failed Landings: {len(self.df) - self.df['Class'].sum()}")
        report.append(f"   Overall Success Rate: {self.df['Class'].mean()*100:.2f}%")
        report.append("")
        
        # Launch site analysis
        report.append("2. LAUNCH SITE ANALYSIS")
        report.append("-" * 70)
        site_stats = self.df.groupby('LaunchSite')['Class'].agg(['count', 'sum', 'mean'])
        for site, stats in site_stats.iterrows():
            report.append(f"   {site}:")
            report.append(f"     - Launches: {stats['count']}")
            report.append(f"     - Success Rate: {stats['mean']*100:.2f}%")
        report.append("")
        
        # Orbit analysis
        report.append("3. ORBIT TYPE ANALYSIS (Top 5 by launch count)")
        report.append("-" * 70)
        orbit_stats = self.df.groupby('Orbit')['Class'].agg(['count', 'sum', 'mean'])
        orbit_stats = orbit_stats.sort_values('count', ascending=False).head(5)
        for orbit, stats in orbit_stats.iterrows():
            report.append(f"   {orbit}:")
            report.append(f"     - Launches: {stats['count']}")
            report.append(f"     - Success Rate: {stats['mean']*100:.2f}%")
        report.append("")
        
        # Feature analysis
        report.append("4. FEATURE IMPACT ANALYSIS")
        report.append("-" * 70)
        for feature in ['GridFins', 'Reused', 'Legs']:
            if feature in self.df.columns:
                success_with = self.df[self.df[feature] == True]['Class'].mean() * 100
                success_without = self.df[self.df[feature] == False]['Class'].mean() * 100
                report.append(f"   {feature}:")
                report.append(f"     - With {feature}: {success_with:.2f}% success rate")
                report.append(f"     - Without {feature}: {success_without:.2f}% success rate")
        report.append("")
        
        report.append("="*70)
        
        report_text = "\n".join(report)
        print("\n" + report_text)
        
        # Save report
        with open('reports/eda_summary.txt', 'w') as f:
            f.write(report_text)
        print("\n✓ Report saved to reports/eda_summary.txt")
        
        return report_text
    
    def run_complete_analysis(self):
        """Run complete EDA analysis and generate all visualizations"""
        print("\n" + "="*60)
        print("STARTING EXPLORATORY DATA ANALYSIS")
        print("="*60)
        
        # Load data
        self.load_data()
        
        # Basic statistics
        self.basic_statistics()
        
        # Create directories for outputs
        import os
        os.makedirs('images', exist_ok=True)
        os.makedirs('reports', exist_ok=True)
        
        print("\nGenerating visualizations...")
        self.plot_success_rate_over_time()
        self.plot_success_by_launch_site()
        self.plot_success_by_orbit()
        self.plot_payload_vs_success()
        self.plot_correlation_heatmap()
        self.plot_feature_importance()
        
        print("\nGenerating summary report...")
        self.generate_summary_report()
        
        print("\n" + "="*60)
        print("EDA COMPLETE!")
        print("="*60)

def main():
    """Main function to run EDA"""
    eda = SpaceXEDA()
    eda.run_complete_analysis()

if __name__ == "__main__":
    main()

