# SEO Tools Setup Guide

## Features Added

### 1. AI-Powered SEO Content Generator
- **Website Categories**: 100+ predefined categories including E-commerce, Technology, Health, Education, etc.
- **AI Generation**: Uses OpenAI API to generate optimized titles, descriptions, and keywords
- **Auto-Copy**: Generated content is automatically copied to clipboard
- **Custom Notification**: Shows "Text Copied" notification with dark navy blue styling

### 2. Enhanced Meta Tags Generator
- **AI Integration**: Same category selection and AI generation as the main SEO generator
- **Manual Input**: Traditional manual input fields for custom content
- **Auto-Generate & Copy**: Generates meta tags and automatically copies them
- **Character Limits**: Built-in character counting for SEO optimization

### 3. Custom Notification System
- **Position**: Center-top of the screen
- **Styling**: Dark navy blue background with rounded corners
- **Animation**: Smooth slide-in animation
- **Duration**: 2-second display time

## Setup Instructions

### 1. Configure OpenAI API Key

1. Copy the example environment file:
   ```bash
   cp .env.example .env
   ```

2. Get your OpenAI API key from [OpenAI Platform](https://platform.openai.com/api-keys)

3. Update the `.env` file:
   ```
   VITE_OPENAI_API_KEY=your_actual_openai_api_key_here
   ```

### 2. Install Dependencies (if needed)
```bash
npm install
```

### 3. Start Development Server
```bash
npm run dev
```

## Usage

### SEO Generator Tab
1. Enter your website name
2. Select from 100+ categories
3. Click "Generate SEO Content"
4. Content is automatically generated and displayed
5. Use copy buttons to copy individual elements

### Meta Tags Tab
1. **AI Generation Section**:
   - Enter website name and select category
   - Click "Generate & Copy Meta Tags"
   - Meta tags are automatically generated and copied

2. **Manual Input Section**:
   - Fill in title, description, and keywords manually
   - Click "Generate & Copy Meta Tags" to copy formatted HTML

### Features
- **Character Limits**: Title (60 chars), Description (160 chars)
- **Keyword Display**: Keywords shown as styled tags
- **Copy Notifications**: Custom "Text Copied" notification appears
- **Error Handling**: Proper error messages for API issues

## File Structure
```
src/
├── data/
│   └── websiteCategories.ts    # 100+ website categories
├── services/
│   └── openaiService.ts        # OpenAI API integration
└── pages/
    └── SeoTools.tsx            # Enhanced SEO tools component
```

## API Usage
The system uses OpenAI's GPT-3.5-turbo model to generate:
- SEO-optimized titles (50-60 characters)
- Meta descriptions (150-160 characters)
- 10 relevant keywords per website category

## Troubleshooting
- **API Key Issues**: Ensure your OpenAI API key is valid and has sufficient credits
- **Generation Errors**: Check browser console for detailed error messages
- **Copy Issues**: Ensure your browser supports the Clipboard API