"""
SpaceX Falcon 9 First Stage Landing Prediction
Part 5: Interactive Dashboard with Plotly Dash

This script creates an interactive dashboard for exploring
SpaceX launch data and landing success patterns.
"""

import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import dash
from dash import dcc, html, Input, Output
import dash_bootstrap_components as dbc

class SpaceXDashboard:
    """Class for creating Plotly Dash dashboard"""
    
    def __init__(self, data_path='data/spacex_launch_data.csv'):
        """Initialize dashboard"""
        self.data_path = data_path
        self.df = None
        self.app = None
        
    def load_data(self):
        """Load launch data"""
        self.df = pd.read_csv(self.data_path)
        self.df['Date'] = pd.to_datetime(self.df['Date'])
        self.df['Year'] = self.df['Date'].dt.year
        print(f"Loaded {len(self.df)} launch records")
        return self.df
    
    def create_success_pie_chart(self):
        """Create pie chart of landing success"""
        success_counts = self.df['Class'].value_counts()
        
        fig = go.Figure(data=[go.Pie(
            labels=['Failed/No Attempt', 'Successful'],
            values=[success_counts.get(0, 0), success_counts.get(1, 0)],
            marker=dict(colors=['#FF6B6B', '#51CF66']),
            textinfo='label+percent',
            hovertemplate='%{label}<br>Count: %{value}<br>Percentage: %{percent}<extra></extra>'
        )])
        
        fig.update_layout(
            title='Overall Landing Success Rate',
            title_font_size=20,
            height=400
        )
        
        return fig
    
    def create_success_over_time(self):
        """Create line chart of success rate over time"""
        yearly_stats = self.df.groupby('Year').agg({
            'Class': ['sum', 'count', 'mean']
        }).reset_index()
        yearly_stats.columns = ['Year', 'Successful', 'Total', 'SuccessRate']
        yearly_stats['SuccessRate'] = yearly_stats['SuccessRate'] * 100
        
        fig = make_subplots(
            rows=1, cols=2,
            subplot_titles=('Success Rate by Year', 'Launch Count by Year'),
            specs=[[{'secondary_y': False}, {'secondary_y': False}]]
        )
        
        # Success rate plot
        fig.add_trace(
            go.Scatter(
                x=yearly_stats['Year'],
                y=yearly_stats['SuccessRate'],
                mode='lines+markers',
                name='Success Rate',
                line=dict(color='green', width=3),
                marker=dict(size=10)
            ),
            row=1, col=1
        )
        
        # Launch count plot
        fig.add_trace(
            go.Bar(
                x=yearly_stats['Year'],
                y=yearly_stats['Total'],
                name='Total Launches',
                marker_color='steelblue'
            ),
            row=1, col=2
        )
        
        fig.update_xaxes(title_text="Year", row=1, col=1)
        fig.update_xaxes(title_text="Year", row=1, col=2)
        fig.update_yaxes(title_text="Success Rate (%)", row=1, col=1)
        fig.update_yaxes(title_text="Number of Launches", row=1, col=2)
        
        fig.update_layout(height=400, showlegend=False, title_text="Launch Trends Over Time")
        
        return fig
    
    def create_launch_site_analysis(self):
        """Create bar chart of success by launch site"""
        site_stats = self.df.groupby('LaunchSite').agg({
            'Class': ['sum', 'count', 'mean']
        }).reset_index()
        site_stats.columns = ['LaunchSite', 'Successful', 'Total', 'SuccessRate']
        site_stats['SuccessRate'] = site_stats['SuccessRate'] * 100
        site_stats = site_stats.sort_values('SuccessRate', ascending=False)
        
        fig = make_subplots(
            rows=1, cols=2,
            subplot_titles=('Success Rate by Launch Site', 'Launch Count by Site')
        )
        
        # Success rate
        fig.add_trace(
            go.Bar(
                y=site_stats['LaunchSite'],
                x=site_stats['SuccessRate'],
                orientation='h',
                name='Success Rate',
                marker_color='green',
                text=site_stats['SuccessRate'].round(1),
                texttemplate='%{text}%',
                textposition='outside'
            ),
            row=1, col=1
        )
        
        # Launch count
        fig.add_trace(
            go.Bar(
                y=site_stats['LaunchSite'],
                x=site_stats['Total'],
                orientation='h',
                name='Total Launches',
                marker_color='steelblue',
                text=site_stats['Total'],
                textposition='outside'
            ),
            row=1, col=2
        )
        
        fig.update_xaxes(title_text="Success Rate (%)", row=1, col=1)
        fig.update_xaxes(title_text="Number of Launches", row=1, col=2)
        
        fig.update_layout(height=400, showlegend=False, title_text="Launch Site Analysis")
        
        return fig
    
    def create_orbit_analysis(self):
        """Create analysis of success by orbit type"""
        orbit_stats = self.df.groupby('Orbit').agg({
            'Class': ['sum', 'count', 'mean']
        }).reset_index()
        orbit_stats.columns = ['Orbit', 'Successful', 'Total', 'SuccessRate']
        orbit_stats = orbit_stats[orbit_stats['Total'] >= 3]  # Filter orbits with at least 3 launches
        orbit_stats['SuccessRate'] = orbit_stats['SuccessRate'] * 100
        orbit_stats = orbit_stats.sort_values('SuccessRate', ascending=True)
        
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            y=orbit_stats['Orbit'],
            x=orbit_stats['SuccessRate'],
            orientation='h',
            marker=dict(
                color=orbit_stats['SuccessRate'],
                colorscale='RdYlGn',
                showscale=True,
                colorbar=dict(title="Success Rate %")
            ),
            text=orbit_stats['SuccessRate'].round(1),
            texttemplate='%{text}%',
            textposition='outside',
            hovertemplate='<b>%{y}</b><br>Success Rate: %{x:.1f}%<br>Total Launches: %{customdata}<extra></extra>',
            customdata=orbit_stats['Total']
        ))
        
        fig.update_layout(
            title='Success Rate by Orbit Type (min 3 launches)',
            xaxis_title='Success Rate (%)',
            yaxis_title='Orbit Type',
            height=500,
            showlegend=False
        )
        
        return fig
    
    def create_payload_analysis(self):
        """Create scatter plot of payload mass vs success"""
        df_payload = self.df[self.df['PayloadMass'] > 0].copy()
        
        fig = px.scatter(
            df_payload,
            x='PayloadMass',
            y='FlightNumber',
            color='Class',
            color_discrete_map={0: 'red', 1: 'green'},
            labels={'Class': 'Landing Success', 'PayloadMass': 'Payload Mass (kg)', 'FlightNumber': 'Flight Number'},
            title='Payload Mass vs Landing Success',
            hover_data=['Name', 'Orbit', 'LaunchSite']
        )
        
        fig.update_traces(marker=dict(size=10, opacity=0.7))
        fig.update_layout(height=400)
        
        return fig
    
    def create_feature_comparison(self):
        """Create comparison of features (GridFins, Reused, Legs)"""
        features = ['GridFins', 'Reused', 'Legs']
        
        fig = make_subplots(
            rows=1, cols=3,
            subplot_titles=('Grid Fins', 'Booster Reused', 'Landing Legs')
        )
        
        for idx, feature in enumerate(features, 1):
            if feature in self.df.columns:
                feature_stats = self.df.groupby(feature)['Class'].agg(['count', 'mean']).reset_index()
                feature_stats['mean'] = feature_stats['mean'] * 100
                
                fig.add_trace(
                    go.Bar(
                        x=['No', 'Yes'],
                        y=feature_stats['mean'].values,
                        marker_color=['red', 'green'],
                        text=feature_stats['mean'].round(1),
                        texttemplate='%{text}%',
                        textposition='outside',
                        showlegend=False
                    ),
                    row=1, col=idx
                )
                
                fig.update_yaxes(title_text="Success Rate (%)", range=[0, 100], row=1, col=idx)
        
        fig.update_layout(height=400, title_text="Impact of Technical Features on Landing Success")
        
        return fig
    
    def create_static_dashboard(self):
        """Create static HTML dashboard with all visualizations"""
        print("\nGenerating dashboard visualizations...")
        
        # Create all figures
        fig1 = self.create_success_pie_chart()
        fig2 = self.create_success_over_time()
        fig3 = self.create_launch_site_analysis()
        fig4 = self.create_orbit_analysis()
        fig5 = self.create_payload_analysis()
        fig6 = self.create_feature_comparison()
        
        # Save figures as HTML
        import os
        os.makedirs('dashboard', exist_ok=True)
        
        fig1.write_html('dashboard/success_pie.html')
        fig2.write_html('dashboard/success_over_time.html')
        fig3.write_html('dashboard/launch_site_analysis.html')
        fig4.write_html('dashboard/orbit_analysis.html')
        fig5.write_html('dashboard/payload_analysis.html')
        fig6.write_html('dashboard/feature_comparison.html')
        
        # Create combined dashboard
        with open('dashboard/spacex_dashboard.html', 'w') as f:
            f.write('''
<!DOCTYPE html>
<html>
<head>
    <title>SpaceX Falcon 9 Landing Analysis Dashboard</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 20px;
            background-color: #f5f5f5;
        }
        .header {
            background-color: #005288;
            color: white;
            padding: 20px;
            text-align: center;
            border-radius: 10px;
            margin-bottom: 20px;
        }
        .dashboard-container {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(600px, 1fr));
            gap: 20px;
        }
        .chart-container {
            background-color: white;
            padding: 15px;
            border-radius: 10px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        iframe {
            width: 100%;
            height: 500px;
            border: none;
        }
    </style>
</head>
<body>
    <div class="header">
        <h1>🚀 SpaceX Falcon 9 Landing Analysis Dashboard</h1>
        <p>Interactive Visual Analytics of First Stage Landing Success</p>
    </div>
    
    <div class="dashboard-container">
        <div class="chart-container">
            <iframe src="success_pie.html"></iframe>
        </div>
        <div class="chart-container">
            <iframe src="success_over_time.html"></iframe>
        </div>
        <div class="chart-container">
            <iframe src="launch_site_analysis.html"></iframe>
        </div>
        <div class="chart-container">
            <iframe src="orbit_analysis.html"></iframe>
        </div>
        <div class="chart-container">
            <iframe src="payload_analysis.html"></iframe>
        </div>
        <div class="chart-container">
            <iframe src="feature_comparison.html"></iframe>
        </div>
    </div>
</body>
</html>
            ''')
        
        print("✓ Dashboard created: dashboard/spacex_dashboard.html")
        print("✓ Individual charts saved in dashboard/ directory")

def main():
    """Main function to create dashboard"""
    print("\n" + "="*70)
    print("CREATING SPACEX PLOTLY DASH DASHBOARD")
    print("="*70)
    
    dashboard = SpaceXDashboard()
    dashboard.load_data()
    dashboard.create_static_dashboard()
    
    print("\n" + "="*70)
    print("DASHBOARD CREATION COMPLETE!")
    print("="*70)
    print("\nOpen 'dashboard/spacex_dashboard.html' in a web browser to view the dashboard.")

if __name__ == "__main__":
    main()

