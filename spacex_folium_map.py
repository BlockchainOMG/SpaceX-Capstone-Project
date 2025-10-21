"""
SpaceX Falcon 9 First Stage Landing Prediction
Part 4: Interactive Visual Analytics with Folium

This script creates interactive maps showing SpaceX launch sites
and landing success patterns.
"""

import pandas as pd
import folium
from folium.plugins import MarkerCluster, MousePosition, HeatMap
import os

class SpaceXFoliumMapping:
    """Class for creating interactive Folium maps of SpaceX launches"""
    
    def __init__(self, data_path='data/spacex_launch_data.csv'):
        """Initialize with data path"""
        self.data_path = data_path
        self.df = None
        
        # Launch site coordinates (approximate)
        self.launch_sites = {
            'CCAFS LC-40': {'lat': 28.5618571, 'lon': -80.577366, 'name': 'Cape Canaveral'},
            'CCAFS SLC-40': {'lat': 28.5618571, 'lon': -80.577366, 'name': 'Cape Canaveral'},
            'KSC LC-39A': {'lat': 28.6080585, 'lon': -80.6039558, 'name': 'Kennedy Space Center'},
            'VAFB SLC-4E': {'lat': 34.632093, 'lon': -120.610829, 'name': 'Vandenberg AFB'},
        }
        
    def load_data(self):
        """Load launch data"""
        self.df = pd.read_csv(self.data_path)
        print(f"Loaded {len(self.df)} launch records")
        return self.df
    
    def create_launch_sites_map(self):
        """Create interactive map of SpaceX launch sites"""
        # Center map on USA
        m = folium.Map(
            location=[37.0902, -95.7129],
            zoom_start=4,
            tiles='OpenStreetMap'
        )
        
        # Add launch sites
        for site_id, site_info in self.launch_sites.items():
            # Count launches from this site
            site_launches = len(self.df[self.df['LaunchSite'] == site_id]) if self.df is not None else 0
            
            # Create popup text
            popup_text = f"""
            <b>{site_info['name']}</b><br>
            Site ID: {site_id}<br>
            Total Launches: {site_launches}
            """
            
            # Add marker
            folium.Marker(
                location=[site_info['lat'], site_info['lon']],
                popup=folium.Popup(popup_text, max_width=300),
                icon=folium.Icon(color='red', icon='rocket', prefix='fa')
            ).add_to(m)
            
            # Add circle
            folium.Circle(
                location=[site_info['lat'], site_info['lon']],
                radius=10000,
                color='blue',
                fill=True,
                fillOpacity=0.2
            ).add_to(m)
        
        # Add mouse position
        MousePosition().add_to(m)
        
        # Save map
        output_path = 'maps/spacex_launch_sites.html'
        m.save(output_path)
        print(f"✓ Saved launch sites map: {output_path}")
        
        return m
    
    def create_success_markers_map(self):
        """Create map with markers colored by landing success"""
        # Center map on USA
        m = folium.Map(
            location=[37.0902, -95.7129],
            zoom_start=4,
            tiles='OpenStreetMap'
        )
        
        # Add markers for each launch
        marker_cluster = MarkerCluster().add_to(m)
        
        for _, launch in self.df.iterrows():
            site_id = launch['LaunchSite']
            if site_id in self.launch_sites:
                site = self.launch_sites[site_id]
                
                # Determine marker color based on landing success
                if pd.notna(launch['LandingSuccess']):
                    if launch['LandingSuccess'] == 1:
                        color = 'green'
                        status = 'Successful'
                    else:
                        color = 'red'
                        status = 'Failed'
                else:
                    color = 'gray'
                    status = 'No landing attempt'
                
                # Create popup
                popup_text = f"""
                <b>{launch.get('Name', 'Unknown')}</b><br>
                Date: {launch.get('Date', 'Unknown')}<br>
                Launch Site: {site['name']}<br>
                Orbit: {launch.get('Orbit', 'Unknown')}<br>
                Landing Status: {status}<br>
                Payload Mass: {launch.get('PayloadMass', 'N/A')} kg
                """
                
                folium.Marker(
                    location=[site['lat'], site['lon']],
                    popup=folium.Popup(popup_text, max_width=300),
                    icon=folium.Icon(color=color, icon='info-sign')
                ).add_to(marker_cluster)
        
        # Add legend
        legend_html = '''
        <div style="position: fixed; 
                    bottom: 50px; right: 50px; width: 180px; height: 110px; 
                    background-color: white; border:2px solid grey; z-index:9999; 
                    font-size:14px; padding: 10px">
        <p><b>Landing Success</b></p>
        <p><i class="fa fa-map-marker fa-2x" style="color:green"></i> Successful</p>
        <p><i class="fa fa-map-marker fa-2x" style="color:red"></i> Failed</p>
        <p><i class="fa fa-map-marker fa-2x" style="color:gray"></i> No Attempt</p>
        </div>
        '''
        m.get_root().html.add_child(folium.Element(legend_html))
        
        # Save map
        output_path = 'maps/spacex_success_markers.html'
        m.save(output_path)
        print(f"✓ Saved success markers map: {output_path}")
        
        return m
    
    def create_distance_markers_map(self):
        """Create map showing distance between launch sites"""
        # Center map on USA
        m = folium.Map(
            location=[37.0902, -95.7129],
            zoom_start=4,
            tiles='CartoDB positron'
        )
        
        # Add launch sites with detailed information
        for site_id, site_info in self.launch_sites.items():
            # Get site statistics
            site_df = self.df[self.df['LaunchSite'] == site_id]
            total_launches = len(site_df)
            successful_landings = site_df['LandingSuccess'].sum() if 'LandingSuccess' in site_df.columns else 0
            success_rate = (successful_landings / total_launches * 100) if total_launches > 0 else 0
            
            # Create detailed popup
            popup_html = f"""
            <div style="width: 200px">
                <h4>{site_info['name']}</h4>
                <b>Site ID:</b> {site_id}<br>
                <b>Coordinates:</b> {site_info['lat']:.4f}, {site_info['lon']:.4f}<br>
                <b>Total Launches:</b> {total_launches}<br>
                <b>Successful Landings:</b> {int(successful_landings)}<br>
                <b>Success Rate:</b> {success_rate:.2f}%
            </div>
            """
            
            folium.Marker(
                location=[site_info['lat'], site_info['lon']],
                popup=folium.Popup(popup_html, max_width=250),
                icon=folium.Icon(color='blue', icon='rocket', prefix='fa'),
                tooltip=site_info['name']
            ).add_to(m)
            
            # Add circle sized by number of launches
            folium.Circle(
                location=[site_info['lat'], site_info['lon']],
                radius=total_launches * 1000,
                color='darkblue',
                fill=True,
                fillColor='lightblue',
                fillOpacity=0.3,
                popup=f"{site_info['name']}<br>{total_launches} launches"
            ).add_to(m)
        
        # Draw lines between launch sites
        sites_list = list(self.launch_sites.values())
        for i in range(len(sites_list)):
            for j in range(i+1, len(sites_list)):
                folium.PolyLine(
                    locations=[
                        [sites_list[i]['lat'], sites_list[i]['lon']],
                        [sites_list[j]['lat'], sites_list[j]['lon']]
                    ],
                    color='red',
                    weight=1,
                    opacity=0.3
                ).add_to(m)
        
        # Save map
        output_path = 'maps/spacex_distance_markers.html'
        m.save(output_path)
        print(f"✓ Saved distance markers map: {output_path}")
        
        return m
    
    def generate_all_maps(self):
        """Generate all Folium maps"""
        print("\n" + "="*70)
        print("GENERATING INTERACTIVE FOLIUM MAPS")
        print("="*70)
        
        # Create maps directory
        os.makedirs('maps', exist_ok=True)
        
        # Load data
        self.load_data()
        
        # Generate maps
        print("\nCreating maps...")
        self.create_launch_sites_map()
        self.create_success_markers_map()
        self.create_distance_markers_map()
        
        print("\n" + "="*70)
        print("MAP GENERATION COMPLETE!")
        print("="*70)
        print("\nGenerated maps:")
        print("  1. maps/spacex_launch_sites.html - Basic launch sites map")
        print("  2. maps/spacex_success_markers.html - Success/failure markers")
        print("  3. maps/spacex_distance_markers.html - Sites with statistics")
        print("\nOpen these HTML files in a web browser to view interactive maps.")

def main():
    """Main function to generate Folium maps"""
    mapper = SpaceXFoliumMapping()
    mapper.generate_all_maps()

if __name__ == "__main__":
    main()

