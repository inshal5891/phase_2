---
name: frontend-skill
description: Build user interfaces by creating pages, components, layouts, and styling. Use for frontend development and UI implementation.
---

# Frontend Skill – Pages, Components & Styling

## Instructions

1. **Page Structure**
   - Define clear page layouts (header, main, footer)
   - Follow routing conventions of the framework (Next.js, React, Vue, etc.)
   - Ensure responsive design for all screen sizes

2. **Component Design**
   - Break UI into reusable components
   - Keep components small and focused
   - Use props/state correctly
   - Maintain separation of concerns

3. **Layout & Styling**
   - Use modern layout systems (Flexbox, Grid)
   - Apply consistent spacing, typography, and colors
   - Support light/dark themes when required
   - Ensure accessibility (ARIA, keyboard navigation)

4. **State & UI Behavior**
   - Handle loading, error, and empty states
   - Manage local and global state efficiently
   - Optimize re-renders and component performance

## Best Practices
- Mobile-first and responsive-first design
- Reusable and composable components
- Consistent design system usage
- Clean and readable markup
- Avoid inline styles when possible

## Example Structure

```html
<main class="layout">
  <header class="site-header">Header</header>

  <section class="content">
    <Card>
      <h1>Page Title</h1>
      <p>Page description goes here</p>
      <button class="primary-btn">Submit</button>
    </Card>
  </section>

  <footer class="site-footer">Footer</footer>
</main>
