# WhatsApp Sender

A desktop application built with Python and Tkinter that allows bulk sending of WhatsApp messages through WhatsApp Web.

## Features

- User-friendly graphical interface
- Excel spreadsheet integration for contact and message management
- Customizable message sending with conditional logic
- Progress tracking and detailed logging
- Random delay between messages for safety
- Chrome WebDriver integration with WhatsApp Web

## Requirements

- Python 3.x
- Chrome Browser
- The following Python packages (installed automatically with requirements.txt):
  - tkinter
  - pandas
  - selenium
  - webdriver_manager
  - openpyxl (for Excel file handling)

## Installation

1. Clone this repository:
```bash
git clone https://github.com/yourusername/whatsapp-sender.git
cd whatsapp-sender
```

2. Create and activate a virtual environment:

On Windows:
```bash
python -m venv venv
venv\Scripts\activate
```

On Linux/MacOS:
```bash
python3 -m venv venv
source venv/bin/activate
```

3. Install required packages:
```bash
pip install -r requirements.txt
```

## Usage

1. Activate the virtual environment (if not already activated)

2. Run the application:
```bash
python whatsapp_sender.py
```

3. Prepare your Excel file with the following columns:
   - Telefone (Phone): Contact numbers
   - Mensagem (Message): Message to be sent
   - Additional columns for conditional sending (using "SIM" as trigger)

4. Select your Excel file in the application

5. Click "Iniciar Envio" (Start Sending) and scan the WhatsApp Web QR code

6. Monitor the progress through the application interface

## Building Executable

To create a standalone executable:

```bash
pip install pyinstaller
pyinstaller --onefile --noconsole whatsapp_sender.py
```

## Development Setup

For development, it's recommended to:

1. Create a new virtual environment:
```bash
python -m venv venv
```

2. Activate the environment:
- Windows: `venv\Scripts\activate`
- Linux/MacOS: `source venv/bin/activate`

3. Install development dependencies:
```bash
pip install -r requirements.txt
```

4. Make your changes

5. Test thoroughly before submitting PR

## Safety and Considerations

- Use this tool responsibly and in accordance with WhatsApp's terms of service
- Be mindful of message frequency to avoid being blocked
- Always test with a small set of numbers first
- Ensure you have permission to message the numbers in your list

## Contributing

Contributions are welcome! Feel free to:
- Report bugs
- Suggest features
- Submit pull requests

## License

This project is licensed under the GNU General Public License v3.0 - see the [LICENSE](LICENSE) file for details.

This means you can:
- Use the software for any purpose
- Change the software
- Share the software
- Share the changes you make

But you must:
- Distribute the source code with the software
- Include the license and copyright notice
- Use the same license for derivative works
- State any changes made to the code

## Author

Alexandre Bialowas

## Disclaimer

This tool is for educational purposes only. Users are responsible for ensuring compliance with WhatsApp's terms of service and applicable laws regarding bulk messaging.
