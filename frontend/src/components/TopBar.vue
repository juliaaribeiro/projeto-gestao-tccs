<template>
  <header class="topbar">
    <div class="topbar-inner">

      <router-link class="brand" to="/">
        <span class="brand-icon">🎓</span>
        <span class="brand-name">Gestão de TCCs</span>
      </router-link>

      <nav class="nav-links">
        <router-link
          v-for="item in navItems"
          :key="item.to"
          :to="item.to"
          class="nav-link"
        >
          <span class="nav-icon">{{ item.icon }}</span>
          {{ item.label }}
        </router-link>
      </nav>

      <button class="hamburger" @click="open = !open" aria-label="Menu">
        <span :class="{ rotated: open }"></span>
        <span :class="{ hidden: open }"></span>
        <span :class="{ rotated2: open }"></span>
      </button>
    </div>

    <nav v-if="open" class="mobile-nav">
      <router-link
        v-for="item in navItems"
        :key="item.to"
        :to="item.to"
        class="mobile-link"
        @click="open = false"
      >
        {{ item.icon }} {{ item.label }}
      </router-link>
    </nav>
  </header>
</template>

<script>
import { ref } from 'vue'

export default {
  setup() {
    const open = ref(false)
    const navItems = [
      { to: '/',             icon: '📊', label: 'Dashboard'    },
      { to: '/alunos',       icon: '🎓', label: 'Alunos'       },
      { to: '/professores',  icon: '👩‍🏫', label: 'Professores'  },
      { to: '/cursos',       icon: '📚', label: 'Cursos'       },
      { to: '/departamentos',icon: '🏢', label: 'Departamentos'},
      { to: '/tccs',         icon: '📄', label: 'TCCs'         },
    ]
    return { open, navItems }
  },
}
</script>

<style scoped>
.topbar {
  background: rgba(9, 14, 28, 0.88);
  backdrop-filter: blur(18px);
  -webkit-backdrop-filter: blur(18px);
  border-bottom: 1px solid var(--border);
  position: sticky;
  top: 0;
  z-index: 100;
}

.topbar-inner {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 0 32px;
  height: 62px;
  max-width: 1400px;
  margin: 0 auto;
}

/* ── Brand ── */
.brand {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-right: 20px;
  flex-shrink: 0;
}

.brand-icon {
  width: 36px;
  height: 36px;
  background: linear-gradient(135deg, var(--indigo), var(--violet));
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.15rem;
}

.brand-name {
  font-weight: 800;
  font-size: 1rem;
  color: var(--text-1);
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
  padding: 7px 12px;
  border-radius: var(--radius-m);
  font-size: 0.875rem;
  font-weight: 500;
  color: var(--text-2);
  transition: background 0.15s, color 0.15s;
  white-space: nowrap;
}
.nav-link:hover { background: rgba(99,102,241,0.1); color: var(--text-1); }
.nav-link.router-link-exact-active {
  background: rgba(99,102,241,0.16);
  color: #a5b4fc;
  font-weight: 600;
}

.nav-icon { font-size: 0.9rem; }

/* ── Hamburger ── */
.hamburger {
  display: none;
  flex-direction: column;
  gap: 5px;
  background: none;
  border: none;
  padding: 8px;
  margin-left: auto;
}
.hamburger span {
  display: block;
  width: 22px;
  height: 2px;
  background: var(--text-2);
  border-radius: 2px;
  transition: transform 0.25s, opacity 0.25s, background 0.2s;
  transform-origin: center;
}
.hamburger:hover span { background: var(--text-1); }
.hamburger span.rotated  { transform: translateY(7px) rotate(45deg); }
.hamburger span.hidden   { opacity: 0; }
.hamburger span.rotated2 { transform: translateY(-7px) rotate(-45deg); }

/* ── Mobile nav ── */
.mobile-nav {
  display: flex;
  flex-direction: column;
  gap: 2px;
  padding: 10px 16px 14px;
  border-top: 1px solid var(--border);
}
.mobile-link {
  padding: 10px 14px;
  border-radius: var(--radius-m);
  color: var(--text-2);
  font-size: 0.9rem;
}
.mobile-link:hover { background: rgba(99,102,241,0.1); color: var(--text-1); }

@media (max-width: 860px) {
  .nav-links { display: none; }
  .hamburger { display: flex; }
  .topbar-inner { padding: 0 20px; }
}
</style>
