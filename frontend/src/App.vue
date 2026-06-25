<template>
  <div class="app-shell">
    <TopBar />
    <main>
      <router-view />
    </main>
    <footer class="app-footer">
      <span>Sistema de Gestão de TCCs — UFLA</span>
      <span class="footer-sep">·</span>
      <span>API:</span>
      <a href="http://127.0.0.1:8000/api/" target="_blank">http://127.0.0.1:8000/api/</a>
    </footer>
  </div>
</template>

<script>
import TopBar from './components/TopBar.vue'
export default { components: { TopBar } }
</script>

<style scoped>
.app-shell {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

main {
  flex: 1;
  padding: 28px 32px;
  max-width: 1400px;
  width: 100%;
  margin: 0 auto;
}

.app-footer {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  padding: 12px 32px;
  font-size: 0.8rem;
  color: var(--text-3);
  border-top: 1px solid var(--border);
  background: var(--surface);
}
.footer-sep { color: var(--border-hover); }
.app-footer a { color: var(--primary); }
.app-footer a:hover { text-decoration: underline; }

@media (max-width: 768px) {
  main { padding: 18px 14px; }
}
</style>
