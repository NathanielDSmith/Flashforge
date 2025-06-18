# FlashForge - Flashcard Web App

A modern, responsive flashcard web application built with Flask and TailwindCSS. Create, manage, and study flashcards with an intuitive interface and smooth flip animations.

## ✨ Features

- **Create Flashcard Sets**: Organize your flashcards into themed sets with titles and descriptions
- **Add Cards**: Easily add question-answer pairs to any set
- **Flip Animation**: Smooth 3D flip animation to reveal answers
- **Study Mode**: Focus on one card at a time with navigation controls
- **Responsive Design**: Works perfectly on desktop, tablet, and mobile devices
- **Modern UI**: Beautiful interface built with TailwindCSS
- **Data Persistence**: Flashcards are saved to a JSON file (no database required)
- **Error Handling**: Comprehensive error handling with user-friendly messages
- **Input Validation**: Robust validation for all user inputs
- **Flash Messages**: Success and error notifications

## 🏗️ Architecture

The application follows modern Flask best practices:

- **Application Factory Pattern**: Modular app creation
- **Configuration Management**: Environment-based configuration
- **Template Partials**: Reusable components
- **Separation of Concerns**: Clean separation between logic, presentation, and data
- **Error Handling**: Comprehensive error pages and validation
- **Type Hints**: Full type annotation support

## 📁 Project Structure

```
flashforge/
├── app.py                 # Main Flask application
├── config.py              # Configuration management
├── requirements.txt       # Python dependencies
├── README.md             # This file
├── flashcards.json       # Data storage (created automatically)
├── static/               # Static assets
│   ├── css/
│   │   └── flashcard.css # Flashcard-specific styles
│   └── js/
│       └── flashcard.js  # JavaScript functionality
└── templates/            # HTML templates
    ├── base.html         # Base template with navigation
    ├── index.html        # Home page
    ├── new_set.html      # Create new set form
    ├── view_set.html     # View and study flashcards
    ├── new_card.html     # Add new card form
    ├── 404.html          # 404 error page
    ├── 500.html          # 500 error page
    └── partials/         # Reusable template components
        ├── navigation.html
        ├── flashcard.html
        ├── study_card.html
        └── empty_state.html
```

## 🚀 Installation

1. **Clone or download the project files**

2. **Activate your virtual environment** (if you have one):
   ```bash
   # Windows
   venv\Scripts\activate
   
   # macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**:
   ```bash
   python app.py
   ```

5. **Open your browser** and go to `http://localhost:5000`

## ⚙️ Configuration

The application uses environment-based configuration:

```bash
# Development (default)
export FLASK_ENV=development

# Production
export FLASK_ENV=production
export SECRET_KEY=your-secret-key-here

# Custom data file location
export DATA_FILE=my_flashcards.json
```

## 📖 Usage

### Creating Your First Set

1. Click "Create New Set" on the home page
2. Enter a title (required) and description (optional)
3. Click "Create Set"

### Adding Cards

1. Open a flashcard set
2. Click "Add Card"
3. Enter your question and answer
4. Click "Add Card"

### Studying

1. Open a flashcard set with cards
2. Click "Enter Study Mode" to focus on one card at a time
3. Use the Previous/Next buttons to navigate
4. Click on cards to flip them and reveal answers
5. Click "Exit Study Mode" to return to the grid view

### Managing Cards and Sets

- **Delete a card**: Click the delete button on the back of any card
- **Delete a set**: Use the delete button in the set header
- **View set details**: See card count and creation date on the home page

## 🔧 Development

### Code Organization

- **Models**: Data management in `FlashcardManager` class
- **Views**: Route handlers with proper error handling
- **Templates**: Jinja2 templates with partials for reusability
- **Static Files**: CSS and JavaScript in separate files
- **Configuration**: Environment-based settings

### Adding Features

The modular structure makes it easy to extend:

1. **New Routes**: Add to `app.py` with proper error handling
2. **New Templates**: Create in `templates/` directory
3. **New Partials**: Add reusable components to `templates/partials/`
4. **New Styles**: Extend `static/css/flashcard.css`
5. **New JavaScript**: Add to `static/js/flashcard.js`

### Testing

```bash
# Run with test configuration
export FLASK_ENV=testing
python app.py
```

## 🎨 Customization

### Styling
The app uses TailwindCSS via CDN and custom CSS. You can customize:
- Colors and themes in `static/css/flashcard.css`
- Layout and components in the template files
- Tailwind configuration in `templates/base.html`

### Data Storage
By default, data is stored in `flashcards.json`. You can modify the `DATA_FILE` configuration to change the storage location.

### Validation Rules
Adjust validation limits in `config.py`:
- `MAX_TITLE_LENGTH`: Maximum set title length
- `MAX_DESCRIPTION_LENGTH`: Maximum description length
- `MAX_QUESTION_LENGTH`: Maximum question length
- `MAX_ANSWER_LENGTH`: Maximum answer length

## 🌐 Browser Compatibility

- Chrome (recommended)
- Firefox
- Safari
- Edge

The flip animations work best in modern browsers that support CSS3 transforms.

## 📝 License

This project is open source and available under the MIT License.

## 🤝 Contributing

Feel free to submit issues, feature requests, or pull requests to improve the application!

### Development Guidelines

1. Follow the existing code structure and patterns
2. Add proper error handling for new features
3. Include input validation where appropriate
4. Use template partials for reusable components
5. Add type hints to new functions
6. Update documentation for new features

## 🐛 Troubleshooting

### Common Issues

1. **Import Errors**: Make sure all dependencies are installed
2. **File Permissions**: Ensure the app can read/write the data file
3. **Port Conflicts**: Change the port in `app.py` if 5000 is in use
4. **Template Errors**: Check that all partial templates exist

### Debug Mode

Enable debug mode for development:
```bash
export FLASK_DEBUG=True
python app.py
``` 