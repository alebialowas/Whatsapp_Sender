# WhatsApp Sender

An automated tool for sending bulk messages through WhatsApp Web.

## Prerequisites

1. Install Git:
   - Visit [git-scm.com](https://git-scm.com/downloads)
   - Download and run the installer for your operating system
   - Windows users: During installation, select "Git from the command line and also from 3rd-party software"
   - Mac users: You can also install via Homebrew: `brew install git`
   - Linux users: Use your package manager:
     ```bash
     # Ubuntu/Debian
     sudo apt-get update
     sudo apt-get install git

     # Fedora
     sudo dnf install git

     # Arch Linux
     sudo pacman -S git
     ```

2. Install Python (version 3.8 or higher):
   - Visit [python.org](https://www.python.org/downloads/)
   - Download the latest Python version for your operating system
   - During installation, check the "Add Python to PATH" option

2. Install Google Chrome:
   - If not already installed, download from [google.com/chrome](https://www.google.com/chrome/)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/alebialowas/Whatsapp_Sender.git
```

2. Navigate to the directory:
```bash
cd Whatsapp_Sender
```

3. Create a virtual environment (recommended):
```bash
python -m venv venv

# Activate the virtual environment:
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate
```

4. Install dependencies:
```bash
pip install -r requirements.txt
```

## How to Use

1. Run the program:
```bash
python main.py
```

2. Select the Excel spreadsheet containing contacts
3. Log in to WhatsApp Web when prompted
4. Click "Start Sending" to begin

## Spreadsheet Structure

The Excel file must follow this format:
- 'Phone' column: Phone numbers (with country/area code)
- 'Message' column: Text to be sent
- Additional columns: Sending conditions (YES/NO)

## Features

- Bulk message sending through WhatsApp Web
- Excel spreadsheet integration
- User-friendly graphical interface
- Progress tracking
- Customizable sending conditions
- Error handling and logging

## Contributing

Contributions are welcome! Feel free to open an issue or submit a pull request.

## Author

Alexandre Bialowas

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contact

For questions or suggestions, please open an [issue](https://github.com/alebialowas/Whatsapp_Sender/issues).
