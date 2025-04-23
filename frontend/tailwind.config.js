// tailwind.config.js
module.exports = {
	content: [
		"./src/**/*.{js,ts,jsx,tsx,mdx}",
		"./app/**/*.{js,ts,jsx,tsx,mdx}",
	],
	theme: {
		extend: {
			colors: {
				primary: {
					DEFAULT: "#10B981",
					50: "#ECFDF5",
					100: "#D1FAE5",
					200: "#A7F3D0",
					300: "#6EE7B7",
					400: "#34D399",
					500: "#10B981",
					600: "#059669",
					700: "#047857",
					800: "#065F46",
					900: "#064E3B",
				},
				secondary: {
					DEFAULT: "#6366F1",
					50: "#EEF2FF",
					100: "#E0E7FF",
					200: "#C7D2FE",
					300: "#A5B4FC",
					400: "#818CF8",
					500: "#6366F1",
					600: "#4F46E5",
					700: "#4338CA",
					800: "#3730A3",
					900: "#312E81",
				},
			},
			textColor: {
				primary: "#10B981",
				secondary: "#6366F1",
			},
			backgroundColor: {
				primary: "#10B981",
				secondary: "#6366F1",
			},
		},
	},
	plugins: [],
};
// tailwind.config.js