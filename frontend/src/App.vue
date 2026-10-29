<template>
  <div class="flex min-h-screen flex-col bg-slate-900 text-white">
    <header class="sticky top-0 z-10 border-b border-slate-800 bg-slate-900/90 backdrop-blur">
      <div class="mx-auto flex max-w-6xl items-center justify-between gap-4 px-4 py-3">
        <RouterLink to="/" class="flex items-center gap-2 text-lg font-bold">
          <span class="rounded-lg bg-blue-500/15 px-2 py-1">🧪</span>
          BioChemVerse
        </RouterLink>
        <nav class="flex items-center gap-1 text-sm">
          <RouterLink to="/" class="nav-link">Beranda</RouterLink>
          <RouterLink to="/modules" class="nav-link">Modul</RouterLink>
        </nav>
      </div>
    </header>

    <main class="flex-1">
      <RouterView />
    </main>

    <footer class="border-t border-slate-800 px-4 py-6 text-center text-xs text-slate-500">
      BioChemVerse · ChemSphere · ForensiLab · AnatomiMed — MIT License
    </footer>
  </div>
</template>
