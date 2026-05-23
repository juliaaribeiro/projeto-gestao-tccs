<template>
  <div class="app-shell">
    <TopBar />
    <main>
      <router-view />
    </main>
    <footer class="app-footer">
      <span>API Django REST:</span>
      <a href="http://127.0.0.1:8000/api/" target="_blank">http://127.0.0.1:8000/api/</a>
    </footer>
  </div>
</template>

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
  padding: 14px 32px;
  font-size: 0.82rem;
  color: var(--text-3);
  border-top: 1px solid var(--border);
}
.app-footer a { color: var(--indigo); transition: color 0.15s; }
.app-footer a:hover { color: var(--cyan); }

@media (max-width: 768px) {
  main { padding: 20px 16px; }
}
</style>
