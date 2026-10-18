import {defineConfig} from '@playwright/test';
export default defineConfig({
  testDir: './e2e', workers: 1, use: {baseURL:'http://127.0.0.1:4200', headless:true},
  webServer: [
    {command:'.venv\\Scripts\\python.exe -m uvicorn backend.app:app --host 127.0.0.1 --port 8000 --no-access-log', cwd:'..', url:'http://127.0.0.1:8000/api/health', timeout:180000, reuseExistingServer:false,
      env:{SOLARI_OFFLINE:'1'}},
    {command:'npm start', url:'http://127.0.0.1:4200', timeout:90000, reuseExistingServer:false}
  ]
});
