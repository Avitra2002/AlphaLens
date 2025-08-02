from core.router import Router
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def main():
    """Main application entry point"""
    router = Router()
    
    print("Financial Analysis System")
    print("=" * 40)
    print("Ask questions about public companies!")
    print("Type 'quit' to exit\n")
    
    while True:
        try:
            query = input("Your question: ").strip()
            
            if query.lower() in ['quit', 'exit', 'q']:
                print("Goodbye!")
                break
                
            if not query:
                continue
                
            print("\nAnalyzing...")
            response = router.process_query(query)
            print(f"\nResponse:\n{response}\n")
            print("-" * 40)
            
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except Exception as e:
            print(f"Error: {e}")
            logging.error(f"Main loop error: {e}")

if __name__ == "__main__":
    main()