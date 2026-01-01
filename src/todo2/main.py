"""
Todo Console Application - Intermediate Level
Entry point for the application
"""

from cli import TodoCLI

def main():
    """Main entry point for the Todo Console Application - Intermediate Level."""
    cli = TodoCLI()
    cli.run()

if __name__ == "__main__":
    main()