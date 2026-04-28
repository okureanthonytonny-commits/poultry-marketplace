# Client Onboarding Checklist

1. Add client as admin in database:
   UPDATE users SET role='admin' WHERE email='client@example.com';

2. Deploy frontend to Vercel (set VITE_API_URL to Render backend).

3. Customize store name, logo, colors (in NavigationBar and Home page).

4. Upload products (via admin panel at /admin/products).

5. Test order flow.