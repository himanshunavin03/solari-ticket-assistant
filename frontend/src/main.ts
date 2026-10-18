import {Component, OnInit, signal, provideZonelessChangeDetection} from '@angular/core';
import {bootstrapApplication} from '@angular/platform-browser';
import {FormsModule} from '@angular/forms';

type Mode = 'keyword' | 'semantic' | 'hybrid';
interface Example {ticket_id: string; subject: string; description: string}
interface Match {ticket: Example & {category: string; tags: string[]; resolution_notes: string}; keyword_score: number; semantic_score: number | null; fusion_score: number | null}
interface Result {outcome: 'matches' | 'no_reliable_match'; matches: Match[]; degraded: boolean; active_mode: Mode; evidence_note: string}

@Component({selector: 'app-root', standalone: true, imports: [FormsModule], templateUrl: './app.html'})
export class App implements OnInit {
  subject = ''; description = ''; mode: Mode = 'hybrid'; example = '';
  examples = signal<Example[]>([]); loading = signal(false); error = signal('');
  result = signal<Result | null>(null); ready = signal('Checking connection');
  degraded = signal(false); count = signal(0);
  private sequence = 0;
  private controller?: AbortController;

  async ngOnInit() {
    try {
      const [health, examples] = await Promise.all([fetch('/api/health'), fetch('/api/examples')]);
      if (!health.ok || !examples.ok) throw new Error();
      const h = await health.json(); this.degraded.set(h.status === 'degraded');
      this.count.set(h.ticket_count); this.ready.set(h.status === 'ready' ? 'Connected' : 'Keyword only');
      this.examples.set((await examples.json()).new_tickets);
      if (this.degraded()) this.mode = 'keyword';
    } catch { this.ready.set('Service unavailable'); this.error.set('Cannot connect to the search service. Start the backend and reload.'); }
  }

  changed() {
    this.sequence++; this.controller?.abort(); this.loading.set(false);
    this.result.set(null); this.error.set('');
  }

  chooseExample() {
    this.changed(); const e = this.examples().find(e => e.ticket_id === this.example);
    if (e) {this.subject = e.subject; this.description = e.description;}
  }

  reset() {this.changed(); this.subject = ''; this.description = ''; this.example = '';}

  async search() {
    this.changed();
    if (!this.subject.trim() || !this.description.trim()) {this.error.set('Enter both a subject and a description.'); return;}
    const sequence = this.sequence; this.controller = new AbortController();
    this.loading.set(true);
    try {
      const response = await fetch('/api/search', {method: 'POST', headers: {'Content-Type':'application/json'},
        body: JSON.stringify({subject: this.subject, description: this.description, mode: this.mode, top_k: 3}),
        signal: this.controller.signal});
      const body = await response.json();
      if (!response.ok) throw new Error(body.error?.message || 'Search unavailable. Please try again.');
      if (sequence === this.sequence) this.result.set(body);
    } catch (error) {
      if (sequence === this.sequence && !(error instanceof DOMException && error.name === 'AbortError'))
        this.error.set(error instanceof Error && !(error instanceof TypeError) ? error.message : 'Search service unavailable. Check the backend connection and retry.');
    } finally {if (sequence === this.sequence) this.loading.set(false);}
  }
}
bootstrapApplication(App, {providers: [provideZonelessChangeDetection()]}).catch(console.error);
