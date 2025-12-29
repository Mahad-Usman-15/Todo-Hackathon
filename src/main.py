"""
Todo Console Application
Entry point for the application
"""

from todo.cli import TodoCLI

def main():
    """Main entry point for the Todo Console Application."""
    cli = TodoCLI()
    cli.run()

if __name__ == "__main__":
    main()