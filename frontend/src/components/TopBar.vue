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
        <ThemePicker />
        <button class="hamburger" @click="open = !open" aria-label="Abrir menu">
          <span :class="{ rotated: open }"></span>
          <span :class="{ hidden: open }"></span>
          <span :class="{ rotated2: open }"></span>
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
import { ref } from 'vue'
import ThemePicker from './ThemePicker.vue'

export default {
  components: { ThemePicker },
  setup() {
    const open = ref(false)
    const navItems = [
      { to: '/',              icon: '📊', label: 'Dashboard'    },
      { to: '/alunos',        icon: '🎓', label: 'Alunos'       },
      { to: '/professores',   icon: '👩‍🏫', label: 'Professores'  },
      { to: '/cursos',        icon: '📚', label: 'Cursos'       },
      { to: '/departamentos', icon: '🏢', label: 'Departamentos'},
      { to: '/tccs',          icon: '📄', label: 'TCCs'         },
    ]
    return { open, navItems }
  },
}
</script>

<style scoped>
.topbar {
  background: #ffffff;
  border-bottom: 2px solid var(--primary);
  position: sticky;
  top: 0;
  z-index: 100;
  box-shadow: 0 2px 8px rgba(15, 26, 46, 0.08);
}

.topbar-inner {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 0 28px;
  height: 58px;
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
  width: 34px;
  height: 34px;
  background: var(--primary);
  border-radius: var(--radius-m);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.1rem;
}

.brand-name {
  font-weight: 800;
  font-size: 0.95rem;
  color: var(--primary);
  letter-spacing: -0.01em;
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
  gap: 5px;
  padding: 6px 11px;
  border-radius: var(--radius-m);
  font-size: 0.85rem;
  font-weight: 500;
  color: var(--text-2);
  transition: background 0.12s, color 0.12s;
  white-space: nowrap;
  text-decoration: none;
}
.nav-link:hover { background: var(--primary-pale); color: var(--primary); text-decoration: none; }
.nav-link.router-link-exact-active {
  background: var(--primary-pale);
  color: var(--primary);
  font-weight: 700;
  border-bottom: 2px solid var(--primary);
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
  display: flex;
  flex-direction: column;
  gap: 2px;
  padding: 8px 16px 12px;
  border-top: 1px solid var(--border);
  background: #fff;
}
.mobile-link {
  padding: 9px 12px;
  border-radius: var(--radius-m);
  color: var(--text-2);
  font-size: 0.9rem;
  text-decoration: none;
  display: flex;
  align-items: center;
  gap: 8px;
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
</style>
