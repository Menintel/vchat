<template>
  <div class="home-page">
    <section class="hero">
      <div class="hero-content">
        <div class="hero-badge glass-card">
          <span class="badge-dot"></span>
          Video conferencing reimagined
        </div>
        <h1 class="hero-title">
          Connect with anyone,
          <span class="text-gradient">anywhere</span>
        </h1>
        <p class="hero-description">
          Crystal-clear video calls, instant room creation, and seamless collaboration. 
          Start your next meeting in seconds.
        </p>
        <div class="hero-actions">
          <RouterLink to="/register" class="btn-modern btn-primary btn-hero">
            Get Started Free
          </RouterLink>
          <RouterLink to="/login" class="btn-modern btn-secondary btn-hero">
            Sign In
          </RouterLink>
        </div>
      </div>
      
      <div class="hero-visual">
        <div class="visual-card glass-card">
          <div class="video-grid">
            <div class="video-tile">
              <div class="tile-avatar" style="background: linear-gradient(135deg, #6366f1, #8b5cf6)">A</div>
            </div>
            <div class="video-tile">
              <div class="tile-avatar" style="background: linear-gradient(135deg, #22d3ee, #6366f1)">B</div>
            </div>
            <div class="video-tile">
              <div class="tile-avatar" style="background: linear-gradient(135deg, #f472b6, #8b5cf6)">C</div>
            </div>
            <div class="video-tile">
              <div class="tile-avatar" style="background: linear-gradient(135deg, #22c55e, #14b8a6)">D</div>
            </div>
          </div>
          <div class="controls-bar">
            <div class="control-dot active"></div>
            <div class="control-dot active"></div>
            <div class="control-dot"></div>
            <div class="control-dot danger"></div>
          </div>
        </div>
      </div>
    </section>

    <section class="features">
      <h2 class="section-title">Why VChat?</h2>
      <div class="features-grid">
        <div class="feature-card glass-card">
          <div class="feature-icon">
            <svg role="img" aria-label="Audio icon" width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <polygon points="11 5 6 9 2 9 2 15 6 15 11 19 11 5"/>
              <path d="M15.54 8.46a5 5 0 0 1 0 7.07"/>
              <path d="M19.07 4.93a10 10 0 0 1 0 14.14"/>
            </svg>
          </div>
          <h3>Crystal Clear Audio</h3>
          <p>AI-powered noise cancellation ensures you're always heard perfectly.</p>
        </div>
        <div class="feature-card glass-card">
          <div class="feature-icon">
            <svg role="img" aria-label="Screen sharing icon" width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <rect x="2" y="3" width="20" height="14" rx="2"/>
              <path d="M8 21h8"/>
              <path d="M12 17v4"/>
            </svg>
          </div>
          <h3>Screen Sharing</h3>
          <p>Share your screen, a window, or specific tabs with a single click.</p>
        </div>
        <div class="feature-card glass-card">
          <div class="feature-icon">
            <svg role="img" aria-label="Unlimited rooms icon" width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M12 2L2 7l10 5 10-5-10-5z"/>
              <path d="M2 17l10 5 10-5"/>
              <path d="M2 12l10 5 10-5"/>
            </svg>
          </div>
          <h3>Unlimited Rooms</h3>
          <p>Create as many rooms as you need, invite anyone to join instantly.</p>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup lang="ts">
// Home page - no special logic needed
</script>

<style scoped>
.home-page {
  padding-top: 80px;
}

.hero {
  min-height: calc(100vh - 80px);
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: var(--space-2xl);
  align-items: center;
  padding: var(--space-2xl) var(--space-xl);
  max-width: 1200px;
  margin: 0 auto;
}

@media (max-width: 1024px) {
  .hero {
    grid-template-columns: 1fr;
    text-align: center;
  }
}

.hero-badge {
  display: inline-flex;
  align-items: center;
  gap: var(--space-sm);
  padding: var(--space-sm) var(--space-md);
  font-size: 0.875rem;
  color: var(--color-text-secondary);
  margin-bottom: var(--space-lg);
}

.badge-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: var(--color-success);
  animation: badge-pulse 2s infinite;
}

@keyframes badge-pulse {
  0%, 100% {
    opacity: 1;
    transform: scale(1);
  }
  50% {
    opacity: 0.5;
    transform: scale(1.1);
  }
}

.hero-title {
  font-size: clamp(2.5rem, 5vw, 4rem);
  font-weight: 700;
  line-height: 1.1;
  margin-bottom: var(--space-lg);
}

.hero-description {
  font-size: 1.125rem;
  color: var(--color-text-secondary);
  max-width: 500px;
  margin-bottom: var(--space-xl);
}

@media (max-width: 1024px) {
  .hero-description {
    margin-left: auto;
    margin-right: auto;
  }
}

.hero-actions {
  display: flex;
  gap: var(--space-md);
  flex-wrap: wrap;
}

@media (max-width: 1024px) {
  .hero-actions {
    justify-content: center;
  }
}

.btn-hero {
  padding: var(--space-md) var(--space-xl);
  font-size: 1rem;
}

.hero-visual {
  display: flex;
  justify-content: center;
}

@media (max-width: 1024px) {
  .hero-visual {
    order: -1;
  }
}

.visual-card {
  padding: var(--space-lg);
  max-width: 400px;
  width: 100%;
}

.video-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: var(--space-md);
  margin-bottom: var(--space-md);
}

.video-tile {
  aspect-ratio: 4/3;
  background: rgba(0, 0, 0, 0.3);
  border-radius: var(--radius-lg);
  display: flex;
  align-items: center;
  justify-content: center;
}

.tile-avatar {
  width: 48px;
  height: 48px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 600;
  font-size: 1.25rem;
  color: white;
}

.controls-bar {
  display: flex;
  justify-content: center;
  gap: var(--space-md);
}

.control-dot {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.1);
  border: 1px solid var(--glass-border);
}

.control-dot.active {
  background: var(--color-primary);
  border-color: var(--color-primary);
}

.control-dot.danger {
  background: var(--color-error);
  border-color: var(--color-error);
}

.features {
  padding: var(--space-2xl);
  max-width: 1200px;
  margin: 0 auto;
}

.section-title {
  text-align: center;
  font-size: 2rem;
  margin-bottom: var(--space-2xl);
}

.features-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: var(--space-lg);
}

.feature-card {
  padding: var(--space-xl);
  text-align: center;
}

.feature-icon {
  width: 64px;
  height: 64px;
  margin: 0 auto var(--space-lg);
  background: var(--gradient-primary);
  border-radius: var(--radius-lg);
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
}

.feature-card h3 {
  margin-bottom: var(--space-sm);
}

.feature-card p {
  color: var(--color-text-muted);
  margin: 0;
}
</style>
