/**
 * API client for communicating with the Railway backend
 */

const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000';
const API_TIMEOUT = parseInt(process.env.NEXT_PUBLIC_API_TIMEOUT || '30000');

interface ApiResponse<T = unknown> {
  data?: T;
  error?: string;
  message?: string;
}

class ApiClient {
  private baseUrl: string;
  private timeout: number;

  constructor(baseUrl: string = API_BASE_URL, timeout: number = API_TIMEOUT) {
    this.baseUrl = baseUrl;
    this.timeout = timeout;
  }

  async request<T>(
    endpoint: string,
    options: RequestInit = {}
  ): Promise<ApiResponse<T>> {
    const url = `${this.baseUrl}${endpoint}`;
    
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), this.timeout);

    try {
      const response = await fetch(url, {
        ...options,
        signal: controller.signal,
        headers: {
          'Content-Type': 'application/json',
          'Accept': 'application/json',
          'Cache-Control': 'no-cache',
          ...options.headers,
        },
      });

      clearTimeout(timeoutId);

      if (!response.ok) {
        const errorText = await response.text();
        throw new Error(`HTTP ${response.status}: ${errorText || response.statusText}`);
      }

      const data = await response.json();
      return { data };
    } catch (error) {
      clearTimeout(timeoutId);
      
      if (error instanceof Error) {
        if (error.name === 'AbortError') {
          return { error: 'Request timeout - please try again' };
        }
        if (error.message.includes('Failed to fetch')) {
          return { error: 'Unable to connect to server - please check your connection' };
        }
        return { error: error.message };
      }
      
      return { error: 'Unknown error occurred' };
    }
  }

  async query(query: string) {
    return this.request('/query', {
      method: 'POST',
      body: JSON.stringify({ query }),
    });
  }

  async getHealth() {
    return this.request('/health');
  }

  async getAgentsStatus() {
    return this.request('/agents/status');
  }

  async getCacheStats() {
    return this.request('/cache/stats');
  }
}

export const apiClient = new ApiClient();
export default apiClient;
