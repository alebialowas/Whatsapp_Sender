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
- The following Python packages:
  - tkinter
  - pandas
  - selenium
  - webdriver_manager
  - openpyxl (for Excel file handling)

## Installation

1. Clone this repository:
```bash
git clone https://github.com/yourusername/whatsapp-sender.git
```

2. Install required packages:
```bash
pip install -r requirements.txt
```

## Usage

1. Run the application:
```bash
python whatsapp_sender.py
```

2. Prepare your Excel file with the following columns:
   - Telefone (Phone): Contact numbers
   - Mensagem (Message): Message to be sent
   - Additional columns for conditional sending (using "SIM" as trigger)

3. Select your Excel file in the application

4. Click "Iniciar Envio" (Start Sending) and scan the WhatsApp Web QR code

5. Monitor the progress through the application interface

## Building Executable

To create a standalone executable:

```bash
pip install pyinstaller
pyinstaller --onefile --noconsole whatsapp_sender.py
```

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

This project is licensed under the MIT License - see the LICENSE file for details.

## Author

Alexandre Bialowas

## Disclaimer

This tool is for educational purposes only. Users are responsible for ensuring compliance with WhatsApp's terms of service and applicable laws regarding bulk messaging.
