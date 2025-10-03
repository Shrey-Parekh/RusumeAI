#!/usr/bin/env python3
"""
Resume Tailoring App - Main Entry Point
"""

from controllers.app_controller import AppController


def main():
    """Main application entry point"""
    try:
        # Create and start the application
        app = AppController()
        app.start_application()
        
    except KeyboardInterrupt:
        print("\nApplication interrupted by user")
    except Exception as e:
        print(f"Application error: {e}")
        raise


if __name__ == "__main__":
    main()