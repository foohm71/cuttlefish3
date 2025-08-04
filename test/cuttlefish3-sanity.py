#!/usr/bin/env python3
"""
Cuttlefish3 Multi-Agent RAG API Sanity Test

This script tests the Cuttlefish3 multi-agent RAG system API with different
routing scenarios to validate intelligent agent selection and response generation.
"""

import requests
import json
import time
import os
import argparse
from typing import Dict, Any, Optional
from datetime import datetime

class Cuttlefish3APITester:
    """Test client for Cuttlefish3 Multi-Agent RAG API."""
    
    def __init__(self, base_url: str, openai_api_key: Optional[str] = None):
        self.base_url = base_url.rstrip('/')
        self.openai_api_key = openai_api_key or os.environ.get('OPENAI_API_KEY')
        self.session = requests.Session()
        
    def health_check(self) -> Dict[str, Any]:
        """Check API health status."""
        print("🔍 Health Check")
        print("-" * 40)
        
        try:
            response = self.session.get(f"{self.base_url}/health", timeout=10)
            response.raise_for_status()
            
            health_data = response.json()
            print(f"✅ API Status: {health_data.get('status', 'unknown')}")
            print(f"   Service: {health_data.get('service', 'unknown')}")
            print(f"   Version: {health_data.get('version', 'unknown')}")
            
            agents = health_data.get('agents', {})
            print(f"   Agents Available:")
            for agent, status in agents.items():
                print(f"     - {agent}: {status}")
            
            return health_data
            
        except requests.exceptions.RequestException as e:
            print(f"❌ Health check failed: {e}")
            return {"status": "error", "error": str(e)}
    
    def test_routing_debug(self, query: str, user_can_wait: bool, production_incident: bool) -> Dict[str, Any]:
        """Test routing decision without full processing."""
        print(f"🧠 Routing Debug Test")
        print(f"   Query: '{query}'")
        print(f"   user_can_wait: {user_can_wait}, production_incident: {production_incident}")
        print("-" * 40)
        
        try:
            payload = {
                "query": query,
                "user_can_wait": user_can_wait,
                "production_incident": production_incident
            }
            
            response = self.session.post(
                f"{self.base_url}/debug/routing",
                json=payload,
                timeout=30
            )
            response.raise_for_status()
            
            debug_data = response.json()
            print(f"✅ Routing Decision: {debug_data.get('routing_decision', 'unknown')}")
            print(f"   Reasoning: {debug_data.get('routing_reasoning', 'unknown')}")
            
            return debug_data
            
        except requests.exceptions.RequestException as e:
            print(f"❌ Routing debug failed: {e}")
            return {"error": str(e)}
    
    def test_multiagent_rag(self, query: str, user_can_wait: bool, production_incident: bool, 
                           test_name: str) -> Dict[str, Any]:
        """Test full multi-agent RAG processing."""
        print(f"🚀 {test_name}")
        print(f"   Query: '{query}'")
        print(f"   user_can_wait: {user_can_wait}, production_incident: {production_incident}")
        print("-" * 40)
        
        start_time = time.time()
        
        try:
            payload = {
                "query": query,
                "user_can_wait": user_can_wait,
                "production_incident": production_incident
            }
            
            # Add OpenAI API key if available
            if self.openai_api_key:
                payload["openai_api_key"] = self.openai_api_key
            
            response = self.session.post(
                f"{self.base_url}/multiagent-rag",
                json=payload,
                timeout=120  # Allow up to 2 minutes for comprehensive search
            )
            response.raise_for_status()
            
            end_time = time.time()
            response_time = end_time - start_time
            
            rag_data = response.json()
            
            # Extract key metrics
            answer = rag_data.get('answer', '')
            context = rag_data.get('context', [])
            metadata = rag_data.get('metadata', {})
            
            # Display results
            print(f"✅ Success! Response time: {response_time:.2f}s")
            print(f"   Routing: {metadata.get('routing_decision', 'unknown')} ({metadata.get('routing_reasoning', 'no reason')})")
            print(f"   Method: {metadata.get('retrieval_method', 'unknown')}")
            print(f"   Processing Time: {metadata.get('processing_time', 0):.2f}s")
            print(f"   Tickets Found: {metadata.get('num_tickets_found', 0)}")
            
            # Show answer preview
            if answer:
                answer_preview = answer[:200] + "..." if len(answer) > 200 else answer
                print(f"   Answer Preview: {answer_preview}")
            else:
                print(f"   ⚠️  No answer generated")
            
            # Show context preview
            if context:
                print(f"   Context Tickets:")
                for i, ticket in enumerate(context[:3]):  # Show first 3
                    key = ticket.get('key', f'Ticket-{i+1}')
                    title = ticket.get('title', 'No title')[:50]
                    print(f"     - {key}: {title}...")
            else:
                print(f"   ⚠️  No context tickets found")
            
            # Add response time to metadata
            rag_data['test_metadata'] = {
                'test_name': test_name,
                'api_response_time': response_time,
                'timestamp': datetime.now().isoformat()
            }
            
            return rag_data
            
        except requests.exceptions.RequestException as e:
            print(f"❌ {test_name} failed: {e}")
            return {"error": str(e), "test_name": test_name}
    
    def run_comprehensive_test(self):
        """Run comprehensive test suite with different scenarios."""
        print("🧪 CUTTLEFISH3 MULTI-AGENT RAG API SANITY TEST")
        print("=" * 80)
        
        # Test query - should work with JIRA data
        test_query = "How to fix memory leaks in XML parser"
        
        results = []
        
        # Health check first
        health_result = self.health_check()
        results.append(("health_check", health_result))
        
        if health_result.get('status') != 'healthy':
            print("\n❌ Health check failed - aborting tests")
            return results
        
        print("\n" + "=" * 80)
        
        # Test 1: Default routing (both flags false)
        print(f"\n🎯 TEST 1: Default Routing")
        routing_debug_1 = self.test_routing_debug(test_query, False, False)
        results.append(("routing_debug_default", routing_debug_1))
        
        rag_result_1 = self.test_multiagent_rag(
            query=test_query,
            user_can_wait=False,
            production_incident=False,
            test_name="Default Routing Test (Fast Response)"
        )
        results.append(("default_routing", rag_result_1))
        
        print("\n" + "=" * 80)
        
        # Test 2: Comprehensive search (user_can_wait = True)
        print(f"\n🎯 TEST 2: Comprehensive Search")
        routing_debug_2 = self.test_routing_debug(test_query, True, False)
        results.append(("routing_debug_comprehensive", routing_debug_2))
        
        rag_result_2 = self.test_multiagent_rag(
            query=test_query,
            user_can_wait=True,
            production_incident=False,
            test_name="Comprehensive Search Test (User Can Wait)"
        )
        results.append(("comprehensive_search", rag_result_2))
        
        print("\n" + "=" * 80)
        
        # Test 3: Production incident (production_incident = True)
        print(f"\n🎯 TEST 3: Production Incident")
        incident_query = "Production system down with ClassCastException"
        routing_debug_3 = self.test_routing_debug(incident_query, False, True)
        results.append(("routing_debug_incident", routing_debug_3))
        
        rag_result_3 = self.test_multiagent_rag(
            query=incident_query,
            user_can_wait=False,
            production_incident=True,
            test_name="Production Incident Test (Urgent Response)"
        )
        results.append(("production_incident", rag_result_3))
        
        # Summary
        self.print_test_summary(results)
        
        return results
    
    def print_test_summary(self, results):
        """Print summary of all test results."""
        print("\n" + "=" * 80)
        print("📊 TEST SUMMARY")
        print("=" * 80)
        
        successful_tests = 0
        total_tests = len([r for r in results if not r[0].startswith('routing_debug')])
        
        for test_name, result in results:
            if test_name.startswith('routing_debug'):
                continue  # Skip routing debug in summary
                
            if 'error' in result:
                print(f"❌ {test_name}: FAILED - {result.get('error', 'Unknown error')}")
            else:
                print(f"✅ {test_name}: SUCCESS")
                successful_tests += 1
                
                # Show key metrics
                metadata = result.get('metadata', {})
                test_metadata = result.get('test_metadata', {})
                
                routing = metadata.get('routing_decision', 'unknown')
                processing_time = metadata.get('processing_time', 0)
                api_time = test_metadata.get('api_response_time', 0)
                tickets = metadata.get('num_tickets_found', 0)
                
                print(f"   Routing: {routing} | Processing: {processing_time:.2f}s | API: {api_time:.2f}s | Tickets: {tickets}")
        
        print(f"\n🎯 OVERALL RESULT: {successful_tests}/{total_tests} tests passed")
        
        if successful_tests == total_tests:
            print("🎉 All tests passed! Cuttlefish3 API is working correctly.")
        else:
            print("⚠️  Some tests failed. Check the logs above for details.")

def main():
    """Main function with command line argument parsing."""
    parser = argparse.ArgumentParser(description="Cuttlefish3 Multi-Agent RAG API Sanity Test")
    parser.add_argument(
        "--host", 
        default="127.0.0.1", 
        help="API host (default: 127.0.0.1)"
    )
    parser.add_argument(
        "--port", 
        type=int, 
        default=5020, 
        help="API port (default: 5000)"
    )
    parser.add_argument(
        "--openai-key",
        help="OpenAI API key (optional, will use OPENAI_API_KEY env var if not provided)"
    )
    parser.add_argument(
        "--protocol",
        choices=["http", "https"],
        default="http",
        help="Protocol to use (default: http)"
    )
    
    args = parser.parse_args()
    
    # Construct base URL
    base_url = f"{args.protocol}://{args.host}:{args.port}"
    
    print(f"🎯 Testing Cuttlefish3 API at: {base_url}")
    print(f"   OpenAI Key: {'Provided' if args.openai_key or os.environ.get('OPENAI_API_KEY') else 'Not provided'}")
    print()
    
    # Create tester and run tests
    tester = Cuttlefish3APITester(base_url, args.openai_key)
    results = tester.run_comprehensive_test()
    
    # Save results to file
    results_file = f"cuttlefish3_sanity_test_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(results_file, 'w') as f:
        json.dump(dict(results), f, indent=2, default=str)
    
    print(f"\n💾 Test results saved to: {results_file}")

if __name__ == "__main__":
    main()
