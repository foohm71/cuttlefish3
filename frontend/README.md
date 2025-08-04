# Cuttlefish3 Frontend

A NextJS frontend for the Cuttlefish3 Multi-Agent RAG System, designed for intelligent JIRA ticket retrieval.

## Features

- **Two-Tab Interface**: Query Tab for interactive searches and Reference Queries Tab for sample questions
- **Toggle Controls**: Configure query behavior with "Not Urgent" and "Production Issue" flags
- **Multi-Agent Integration**: Connects to the Cuttlefish3 multi-agent RAG API
- **Responsive Design**: Modern, clean UI built with Tailwind CSS
- **Configurable API**: Environment-based API URL configuration

## Quick Start

1. **Install Dependencies**:
   ```bash
   cd frontend
   npm install
   ```

2. **Configure API URL**:
   Copy the environment template and update the API URL:
   ```bash
   cp .env.local.template .env.local
   # Edit .env.local and set NEXT_PUBLIC_API_URL to your API endpoint
   ```

3. **Run Development Server**:
   ```bash
   npm run dev
   ```
   
   Open [http://localhost:3000](http://localhost:3000) in your browser.

## Configuration

### Environment Variables

Create a `.env.local` file in the frontend directory:

```env
NEXT_PUBLIC_API_URL=http://127.0.0.1:5020
```

### API Integration

The frontend connects to the Cuttlefish3 multi-agent RAG system via the `/multiagent-rag` endpoint. The API expects:

```json
{
  "query": "Your JIRA ticket query",
  "user_can_wait": true,
  "production_incident": false
}
```

## Usage

### Query Tab

1. **Toggle Settings**:
   - **Not Urgent**: When enabled, allows the system to use more comprehensive but slower retrieval methods
   - **Production Issue**: When enabled, prioritizes speed and uses emergency routing for critical incidents

2. **Query Input**: Enter your JIRA ticket search query
3. **Submit**: Click "Search JIRA Tickets" or use Cmd/Ctrl + Enter
4. **Results**: View the AI-generated answer, related tickets, and query metadata

### Reference Queries Tab

Browse sample questions organized by categories:
- Technical Troubleshooting
- Bug Pattern Recognition
- Framework-Specific Issues
- Production Incident Analysis
- And more...

## Architecture

- **Frontend**: NextJS 14 with TypeScript
- **Styling**: Tailwind CSS with custom components
- **State Management**: React hooks
- **API Integration**: Fetch API with error handling
- **Markdown Rendering**: react-markdown for reference content

## Development

### Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run start` - Start production server
- `npm run lint` - Run ESLint

### Project Structure

```
frontend/
├── src/
│   └── app/
│       ├── globals.css
│       ├── layout.tsx
│       └── page.tsx
├── public/
│   └── cuttlefish.svg
├── .env.local.template
├── package.json
└── README.md
```

## Integration with Cuttlefish3 API

The frontend is designed to work with the Cuttlefish3 multi-agent RAG system. Ensure your API server is running before using the frontend:

1. Start the Cuttlefish3 Flask server (typically on port 5020)
2. Update the `NEXT_PUBLIC_API_URL` in your `.env.local` file
3. The frontend will automatically connect to the configured API endpoint

## Customization

### Toggle Labels
The toggle switches can be customized by modifying the labels in `src/app/page.tsx`:
- "Not Urgent" maps to `user_can_wait` API parameter
- "Production Issue" maps to `production_incident` API parameter

### Styling
The UI uses Tailwind CSS with custom toggle switch styling. Modify `src/app/globals.css` to customize the appearance.

### Sample Questions
The Reference Queries tab displays content from the embedded `SAMPLE_QUESTIONS` constant. This can be updated to reflect your specific use cases.