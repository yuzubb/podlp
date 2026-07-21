const { generate } = require('youtube-po-token-generator');

(async () => {
  try {
    const result = await generate();
    console.log(JSON.stringify({
      status: 'success',
      poToken: result.poToken,
      visitorData: result.visitorData
    }));
  } catch (err) {
    console.log(JSON.stringify({
      status: 'error',
      message: err.message
    }));
    process.exit(1);
  }
})();
