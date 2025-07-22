export default defineNuxtRouteMiddleware((to) => {
  const redirectFrom = [
    "/contact",
    "/kontakt",
    "/impressum",
    "/privacy",
    "/imprint",
  ];
  const redirectTo = "/legal";

  if (redirectFrom.includes(to.path)) {
    return navigateTo(redirectTo);
  }
});
