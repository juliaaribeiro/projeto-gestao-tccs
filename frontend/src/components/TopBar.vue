<template>
  <header class="topbar">
    <div class="topbar-inner">

      <router-link class="brand" to="/">
        <div class="brand-icon" aria-hidden="true">🎓</div>
        <span class="brand-name">Gestão de TCCs</span>
      </router-link>

      <nav class="nav-links" aria-label="Navegação principal">
        <router-link
          v-for="item in navItems"
          :key="item.to"
          :to="item.to"
          class="nav-link"
        >
          <span class="nav-icon" aria-hidden="true">{{ item.icon }}</span>
          {{ item.label }}
        </router-link>
      </nav>

      <div class="topbar-end">
       <button
          class="font-btn"
          @click="decreaseFont"
          title="Diminuir fonte"
        >
          A-
        </button>

        <button
          class="font-btn"
          @click="increaseFont"
          title="Aumentar fonte"
        >
          A+
        </button>

        <ThemePicker />

        <button
          class="hamburger"
          @click="open = !open"
          aria-label="Abrir menu"
        >
        </button>
      </div>
    </div>

    <nav v-if="open" class="mobile-nav" aria-label="Menu mobile">
      <router-link
        v-for="item in navItems"
        :key="item.to"
        :to="item.to"
        class="mobile-link"
        @click="open = false"
      >
        <span aria-hidden="true">{{ item.icon }}</span> {{ item.label }}
      </router-link>
      <div class="mobile-theme">
        <ThemePicker />
      </div>
    </nav>
  </header>
</template>

<script>
import { ref, onMounted } from 'vue'
import ThemePicker from './ThemePicker.vue'

export default {
  components: { ThemePicker },
  setup() {
    const open = ref(false)
    const navItems = [
      { to: '/', label: 'Dashboard'},
      { to: '/alunos', label: 'Alunos'},
      { to: '/professores', label: 'Professores'},
      { to: '/cursos', label: 'Cursos'},
      { to: '/departamentos', label: 'Departamentos'},
      { to: '/tccs', label: 'TCCs'},
    ]
    const applyFontScale = (scale) => {
      document.documentElement.style.setProperty(
        '--font-scale',
        scale
      )
    }

    const increaseFont = () => {
      let current = Number(
        localStorage.getItem('fontScale') || '1'
      )

      current = Math.min(current + 0.1, 1.5)

      localStorage.setItem('fontScale', current)

      applyFontScale(current)
    }

    const decreaseFont = () => {
      let current = Number(
        localStorage.getItem('fontScale') || '1'
      )

      current = Math.max(current - 0.1, 0.8)

      localStorage.setItem('fontScale', current)

      applyFontScale(current)
    }

    onMounted(() => {
      const scale = Number(
        localStorage.getItem('fontScale') || '1'
      )

      applyFontScale(scale)
    })

    return {open, navItems, increaseFont, decreaseFont}
  },
}
</script>

<style scoped>
.topbar {
  background: var(--surface);
  border-bottom: 2px solid var(--primary);
  position: sticky;
  top: 0;
  z-index: 100;
  box-shadow: 0 2px 8px rgba(15, 26, 46, 0.08);
}

.topbar-inner {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 0 32px;
  height: 72px;
  max-width: 1400px;
  margin: 0 auto;
}

/* ── Brand ── */
.brand {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-right: 24px;
  flex-shrink: 0;
  text-decoration: none;
}
.brand:hover { text-decoration: none; }

.brand-icon {
  width: 42px;
  height: 42px;
  background: var(--primary);
  color: white;
  border-radius: var(--radius-m);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.95rem;
  font-weight: 700;
}

.brand-name {
  font-weight: 800;
  font-size: 1.2rem;
  color: var(--text-1);
}

/* ── Nav ── */
.nav-links {
  display: flex;
  align-items: center;
  gap: 2px;
  flex: 1;
}

.nav-link {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 10px 16px;
  border-radius: var(--radius-m);
  font-size: 1rem;
  font-weight: 600;
  color: var(--text-2);
  transition: all 0.2s ease;
  white-space: nowrap;
  text-decoration: none;
}

.nav-link:hover {
  background: var(--primary-pale);
  color: var(--primary);
}

.nav-link.router-link-exact-active {
  background: var(--primary-pale);
  color: var(--primary);
  font-weight: 700;
  border-bottom: 3px solid var(--primary);
}

.nav-icon { font-size: 0.85rem; }

/* ── End area ── */
.topbar-end {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-left: auto;
}

/* ── Hamburger ── */
.hamburger {
  display: none;
  flex-direction: column;
  gap: 5px;
  background: none;
  border: none;
  padding: 7px;
}
.hamburger span {
  display: block;
  width: 20px;
  height: 2px;
  background: var(--text-2);
  border-radius: 2px;
  transition: transform 0.22s, opacity 0.22s;
  transform-origin: center;
}
.hamburger:hover span { background: var(--primary); }
.hamburger span.rotated  { transform: translateY(7px) rotate(45deg); }
.hamburger span.hidden   { opacity: 0; }
.hamburger span.rotated2 { transform: translateY(-7px) rotate(-45deg); }

/* ── Mobile nav ── */
.mobile-nav {
  background: var(--surface);
}
.mobile-link {
  padding: 12px 14px;
  border-radius: var(--radius-m);
  color: var(--text-2);
  font-size: 1rem;
  font-weight: 600;
  text-decoration: none;
}
.mobile-link:hover { background: var(--primary-pale); color: var(--primary); text-decoration: none; }
.mobile-theme {
  padding: 10px 12px 4px;
  border-top: 1px solid var(--border);
  margin-top: 4px;
}

@media (max-width: 860px) {
  .nav-links { display: none; }
  .hamburger { display: flex; }
  .topbar-inner { padding: 0 16px; }
}

.font-btn {
  width: 36px;
  height: 36px;

  border: 1px solid var(--border);
  border-radius: var(--radius-m);

  background: var(--surface);
  color: var(--text-1);

  font-weight: 700;
  cursor: pointer;

  transition: all 0.2s ease;
}

.font-btn:hover {
  background: var(--primary-pale);
  border-color: var(--primary);
}

</style>
