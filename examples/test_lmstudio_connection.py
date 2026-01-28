"""
Quick test script to verify LM Studio connection
Run this AFTER starting LM Studio's local server
"""
import requests
import sys

def test_lmstudio_connection():
    """Test if LM Studio is running and accessible"""
    
    endpoint = "http://localhost:1234/v1/models"
    
    print("🔍 Testing LM Studio Connection...")
    print(f"   Endpoint: {endpoint}\n")
    
    try:
        response = requests.get(endpoint, timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            print("✅ LM Studio is running!")
            print(f"   Status: Connected")
            
            if 'data' in data and len(data['data']) > 0:
                print(f"   Models loaded: {len(data['data'])}")
                for model in data['data']:
                    print(f"     - {model.get('id', 'Unknown')}")
            else:
                print("   ⚠️  No models loaded yet")
                print("   → Load a model in LM Studio before running examples")
            
            print("\n✅ Ready to run OpenAspen examples!")
            return True
        else:
            print(f"❌ Unexpected response: {response.status_code}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ Connection Failed!")
        print("\n📋 Troubleshooting Steps:")
        print("   1. Open LM Studio application")
        print("   2. Go to 'Local Server' tab (left sidebar)")
        print("   3. Select a model from the dropdown")
        print("   4. Click 'Start Server'")
        print("   5. Wait for 'Server running on http://localhost:1234'")
        print("   6. Run this test again")
        return False
        
    except requests.exceptions.Timeout:
        print("❌ Connection Timeout!")
        print("   LM Studio might be starting up, try again in a moment")
        return False
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


if __name__ == "__main__":
    print("=" * 60)
    print("  LM Studio Connection Test")
    print("=" * 60 + "\n")
    
    success = test_lmstudio_connection()
    
    print("\n" + "=" * 60)
    
    if success:
        print("\n🚀 Next step: Run the full example")
        print("   python examples/lmstudio_example.py")
    else:
        print("\n⚠️  Fix the connection issue above first")
    
    sys.exit(0 if success else 1)
