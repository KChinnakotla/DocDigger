import React, { useState } from 'react';
import './index.css'

function App() {
    const [url, setUrl] = useState('');
    const [pdfLinks, setPdfLinks] = useState([]);
    const [loading, setLoading] = useState(false);

    const handleScrape = async () => {
        try {
            setLoading(true);
            const fullURL = "http://localhost:5000/scrape?url=\"" + url + "\""
            console.log(fullURL)
            const response = await fetch(fullURL)

            if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`);
            }

            const data = await response.json();
            setPdfLinks(data.pdfs);
            setLoading(false);
        } catch (error) {
            console.error("Error scraping PDFs:", error);
        }
    };

    return (
        <div>
            <h1>DocDigger</h1>
            <input 
                type="text" 
                value={url} 
                onChange={(e) => setUrl(e.target.value)} 
                placeholder="Enter URL to scrape"
            />
            <button onClick={handleScrape}>Scrape PDFs</button>
            <h2>Found PDFs:</h2>
            {!loading ? (<ul>
                {pdfLinks.map((pdf, index) => (
                    <li key={index}><a href={pdf} target="_blank" rel="noopener noreferrer">{pdf}</a></li>
                ))}
            </ul>)
            : (
                <div className="spinner"></div>
            )}
        </div>
    );
}

export default App;
