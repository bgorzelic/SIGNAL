#!/usr/bin/env python3

import os
import json
from google.cloud import service_management_v1
from google.oauth2 import service_account

class GoogleCloudAPIDiscovery:
    def __init__(self, service_account_path=None):
        """
        Initialize Google Cloud API Discovery
        
        :param service_account_path: Path to service account JSON
        """
        self.service_account_path = service_account_path
        self.credentials = None
        self.service_management_client = None
        
        self._authenticate()

    def _authenticate(self):
        """
        Authenticate with Google Cloud
        """
        if not self.service_account_path or not os.path.exists(self.service_account_path):
            print("Warning: No valid service account path provided")
            return
        
        try:
            # Load credentials from service account file
            self.credentials = service_account.Credentials.from_service_account_file(
                self.service_account_path,
                scopes=['https://www.googleapis.com/auth/cloud-platform']
            )
            
            # Initialize Service Management Client
            self.service_management_client = service_management_v1.ServiceManagerClient(
                credentials=self.credentials
            )
            
            print("Successfully authenticated with Google Cloud")
        except Exception as e:
            print(f"Authentication failed: {e}")

    def list_enabled_apis(self):
        """
        List currently enabled APIs for the project
        
        :return: List of enabled APIs
        """
        if not self.service_management_client:
            print("Service management client not initialized")
            return []
        
        try:
            # Get project ID from credentials
            project_id = self.credentials.project_id
            
            # List enabled services
            request = service_management_v1.ListServicesRequest(
                consumer=f'projects/{project_id}'
            )
            
            response = self.service_management_client.list_services(request=request)
            
            enabled_apis = []
            for service in response:
                enabled_apis.append({
                    'name': service.service_name,
                    'state': service.state
                })
            
            return enabled_apis
        except Exception as e:
            print(f"Error listing APIs: {e}")
            return []

    def recommended_apis_for_signal(self):
        """
        Recommended APIs for SIGNAL network intelligence platform
        
        :return: List of recommended APIs
        """
        return [
            # Compute and Storage
            'compute.googleapis.com',
            'storage.googleapis.com',
            
            # Data and Analytics
            'bigquery.googleapis.com',
            'dataflow.googleapis.com',
            'pubsub.googleapis.com',
            
            # Machine Learning
            'ml.googleapis.com',
            'aiplatform.googleapis.com',
            'vertex.googleapis.com',
            
            # Monitoring and Logging
            'monitoring.googleapis.com',
            'logging.googleapis.com',
            
            # Advanced Intelligence
            'vision.googleapis.com',
            'language.googleapis.com'
        ]

    def check_api_status(self, api_name):
        """
        Check specific API status
        
        :param api_name: API service name
        :return: API status details
        """
        if not self.service_management_client:
            return {"error": "Service management client not initialized"}
        
        try:
            project_id = self.credentials.project_id
            request = service_management_v1.GetServiceRequest(
                service_name=api_name,
                consumer=f'projects/{project_id}'
            )
            
            service = self.service_management_client.get_service(request=request)
            
            return {
                'name': service.service_name,
                'state': service.state,
                'config': service.config
            }
        except Exception as e:
            return {"error": str(e)}

def main():
    # Path to service account key (replace with actual path)
    service_account_path = '/path/to/service_account.json'
    
    # Initialize API Discovery
    api_discovery = GoogleCloudAPIDiscovery(service_account_path)
    
    # List currently enabled APIs
    print("Enabled APIs:")
    enabled_apis = api_discovery.list_enabled_apis()
    for api in enabled_apis:
        print(f"- {api['name']}: {api['state']}")
    
    # Check recommended APIs
    print("\nRecommended APIs for SIGNAL:")
    for api in api_discovery.recommended_apis_for_signal():
        status = api_discovery.check_api_status(api)
        print(f"- {api}: {status.get('state', 'Unknown')}")

if __name__ == "__main__":
    main()