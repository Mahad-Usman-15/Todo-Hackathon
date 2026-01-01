"""
Todo Console Application - Basic Level
Entry point for the application
"""

from todo.cli import TodoCLI

def main():
    """Main entry point for the Todo Console Application - Basic Level."""
    cli = TodoCLI()
    cli.run()

if __name__ == "__main__":
    main()