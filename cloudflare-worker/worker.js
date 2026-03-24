/**
 * Cloudflare Worker - YouTube Shorts Automation Scheduler
 * 
 * This worker triggers GitHub Actions workflows at precise times using Cloudflare Cron Triggers.
 * No delays, runs at exact scheduled times.
 */

export default {
  // Handle scheduled cron triggers
  async scheduled(event, env, ctx) {
    console.log('Cron trigger fired at:', new Date().toISOString());
    
    try {
      // Trigger GitHub Actions workflow
      const result = await triggerGitHubWorkflow(env);
      
      console.log('GitHub workflow triggered successfully:', result);
      
    } catch (error) {
      console.error('Failed to trigger GitHub workflow:', error);
      throw error;
    }
  },

  // Handle HTTP requests (for manual testing)
  async fetch(request, env, ctx) {
    const url = new URL(request.url);
    
    // Health check endpoint
    if (url.pathname === '/health') {
      return new Response(JSON.stringify({
        status: 'ok',
        message: 'YouTube Shorts Automation Worker is running',
        timestamp: new Date().toISOString()
      }), {
        headers: { 'Content-Type': 'application/json' }
      });
    }
    
    // Manual trigger endpoint
    if (url.pathname === '/trigger' && request.method === 'POST') {
      try {
        const result = await triggerGitHubWorkflow(env);
        
        return new Response(JSON.stringify({
          success: true,
          message: 'GitHub workflow triggered successfully',
          result: result
        }), {
          status: 200,
          headers: { 'Content-Type': 'application/json' }
        });
        
      } catch (error) {
        return new Response(JSON.stringify({
          success: false,
          error: error.message
        }), {
          status: 500,
          headers: { 'Content-Type': 'application/json' }
        });
      }
    }
    
    // Default response
    return new Response(JSON.stringify({
      message: 'YouTube Shorts Automation Worker',
      endpoints: {
        health: '/health',
        trigger: '/trigger (POST)'
      }
    }), {
      headers: { 'Content-Type': 'application/json' }
    });
  }
};

/**
 * Trigger GitHub Actions workflow via repository dispatch
 */
async function triggerGitHubWorkflow(env) {
  const GITHUB_TOKEN = env.GITHUB_TOKEN;
  const GITHUB_REPO = env.GITHUB_REPO; // Format: "username/repo"
  
  if (!GITHUB_TOKEN) {
    throw new Error('GITHUB_TOKEN environment variable not set');
  }
  
  if (!GITHUB_REPO) {
    throw new Error('GITHUB_REPO environment variable not set');
  }
  
  const url = `https://api.github.com/repos/${GITHUB_REPO}/dispatches`;
  
  const response = await fetch(url, {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${GITHUB_TOKEN}`,
      'Accept': 'application/vnd.github.v3+json',
      'Content-Type': 'application/json',
      'User-Agent': 'Cloudflare-Worker-YouTube-Automation'
    },
    body: JSON.stringify({
      event_type: 'generate-video'
    })
  });
  
  if (!response.ok) {
    const errorText = await response.text();
    throw new Error(`GitHub API error (${response.status}): ${errorText}`);
  }
  
  return {
    status: response.status,
    message: 'Workflow triggered successfully',
    timestamp: new Date().toISOString()
  };
}
