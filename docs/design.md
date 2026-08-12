# UI Design System & Styling Guide

## 1. Design Philosophy
Clean, authoritative, accessible, and responsive. Focuses on visual item cards, clear location tags, and explicit safety consent dialogs.

---

## 2. Color Palette Tokens (Tailwind CSS)

| Token Role | Tailwind Class | Color Hex | Application |
| :--- | :--- | :--- | :--- |
| **Primary Brand** | `slate-900` | `#0F172A` | Navigation bar, headers, dark buttons |
| **Accent Brand** | `indigo-600` | `#4F46E5` | Active states, primary action buttons, focused rings |
| **Background** | `slate-50` | `#F8FAFC` | Page body background |
| **Card Surface** | `white` | `#FFFFFF` | Content cards, modal overlays, form panels |
| **Lost Tag** | `amber-600` | `#D97706` | Lost item badges & warning prompts |
| **Success Emerald** | `emerald-600` | `#059669` | Found badges, resolved tags, Karma point indicators |
| **Primary Text** | `slate-900` | `#0F172A` | Main headings, body copy |
| **Muted Text** | `slate-500` | `#64748B` | Subtitles, helper text, timestamps |

---

## 3. Typography Scale
- **Display Heading:** `text-3xl font-extrabold tracking-tight text-slate-900`
- **Section Title:** `text-xl font-bold text-slate-800`
- **Card Header:** `text-lg font-semibold text-slate-900`
- **Body Text:** `text-sm font-normal text-slate-700 leading-relaxed`
- **Caption / Meta:** `text-xs font-medium text-slate-500`

---

## 4. Reusable UI Elements

### Item Card Pattern
```html
<div class="bg-white rounded-xl border border-slate-200 shadow-sm hover:shadow-md transition p-5 flex flex-col justify-between">
  <div class="flex justify-between items-center mb-3">
    <span class="bg-emerald-100 text-emerald-800 text-xs font-semibold px-2.5 py-0.5 rounded-full">FOUND</span>
    <span class="text-xs text-slate-500">Admin Block • Floor 1</span>
  </div>
  <h3 class="text-lg font-semibold text-slate-900 mb-1">Black AirPods Case</h3>
  <p class="text-sm text-slate-600 mb-4">Found near Row 2 desks in the reading hall.</p>
  <a href="/items/1" class="text-center bg-slate-900 hover:bg-slate-800 text-white text-sm font-medium py-2 rounded-lg transition">View Details & Claim</a>
</div>
```
