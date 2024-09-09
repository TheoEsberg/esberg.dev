let darkmode = localStorage.getItem("darkmode");
const themeSwitch = document.getElementById("theme-switch");

const enableDarkmode = () => {
  document.body.classList.add("darkmode");
  localStorage.setItem("darkmode", "active");
};

const disableDarkmode = () => {
  document.body.classList.remove("darkmode");
  localStorage.setItem("darkmode", "");
};

if (darkmode === "active") {
  enableDarkmode();
} else if (window.matchMedia("(prefers-color-scheme: dark)")) {
  enableDarkmode();
} else if (window.matchMedia("(prefers-color-scheme: light)")) {
  disableDarkmode();
} else {
  disableDarkmode;
}

themeSwitch.addEventListener("click", () => {
  darkmode = localStorage.getItem("darkmode");
  darkmode !== "active" ? enableDarkmode() : disableDarkmode();
});
