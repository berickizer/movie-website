const fs = require('fs');
const fetch = require('node-fetch');

const API_KEY = 'df028524da0623bdda47c7fd0504b092';
const BASE_URL = 'https://api.themoviedb.org/3';
const IMAGE_URL = 'https://image.tmdb.org/t/p/w500';

const fetchLatestItems = async () => {
  const urls = [
    `${BASE_URL}/movie/upcoming?api_key=${API_KEY}&language=en-US&page=1`,
    `${BASE_URL}/tv/popular?api_key=${API_KEY}&language=en-US&page=1`
  ];

  const htmlBlocks = [];

  for (const url of urls) {
    const res = await fetch(url);
    const data = await res.json();

    const isMovie = url.includes('/movie/');
    const items = data.results.slice(0, 5);

    items.forEach(item => {
      const title = isMovie ? item.title : item.name;
      const overview = item.overview || 'No description available.';
      const imagePath = item.poster_path ? `${IMAGE_URL}${item.poster_path}` : '';
      const googleSearch = `https://www.google.com/search?q=${encodeURIComponent(title + (isMovie ? ' movie' : ' tv show'))}`;

      const block = `
        <div style="background-color:#1e1e1e; padding:20px; border-radius:15px; margin:20px auto; max-width:700px; box-shadow:0 4px 12px rgba(0,0,0,0.5);">
          ${imagePath ? `<img src="${imagePath}" alt="${title}" style="width:100%; border-radius:10px; margin-bottom:15px;">` : ''}
          <h3 style="color:#00ffcc;">${title} (${isMovie ? 'Movie' : 'TV Show'})</h3>
          <p><strong>Overview:</strong> ${overview}</p>
          <a href="${googleSearch}" target="_blank" style="display:inline-block; margin-top:10px; padding:10px 20px; background-color:#00ffcc; color:#121212; text-decoration:none; border-radius:20px; font-weight:bold;">More Info 🔍</a>
        </div>
      `;

      htmlBlocks.push(block);
    });
  }

  const fullHTML = `
    <!DOCTYPE html>
    <html>
    <head>
      <title>Latest - Fakira Movie Zone</title>
      <meta charset="UTF-8">
      <meta name="viewport" content="width=device-width, initial-scale=1">
      <link rel="stylesheet" href="style.css">
    </head>
    <body>
      <div style="background-color: #1e1e1e; padding: 15px; text-align: center;">
        <a href="index.html" style="display: inline-block; margin: 0 10px; padding: 10px 20px; background-color: #00ffcc; color: #121212; text-decoration: none; border-radius: 20px; font-weight: bold;">🏠 Home</a>
        <a href="movies.html" style="display: inline-block; margin: 0 10px; padding: 10px 20px; background-color: #00ffcc; color: #121212; text-decoration: none; border-radius: 20px; font-weight: bold;">🎬 Movies</a>
        <a href="tvshows.html" style="display: inline-block; margin: 0 10px; padding: 10px 20px; background-color: #00ffcc; color: #121212; text-decoration: none; border-radius: 20px; font-weight: bold;">📺 TV Shows</a>
        <a href="latest.html" style="display: inline-block; margin: 0 10px; padding: 10px 20px; background-color: #00ffcc; color: #121212; text-decoration: none; border-radius: 20px; font-weight: bold;">🆕 Latest</a>
      </div>

      <h2 style="text-align: center; color: #00ffcc; margin-top: 30px;">🆕 Latest Releases</h2>
      ${htmlBlocks.join('\n')}
    </body>
    </html>
  `;

  fs.writeFileSync('latest.html', fullHTML);
  console.log('✅ Latest content updated in latest.html');
};

fetchLatestItems();
