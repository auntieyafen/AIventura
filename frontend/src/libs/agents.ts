export async function handleAgentPlan(message: string) {
    // 這邊可以之後拆成：
    // 1. WebSearchAgent(message)
    // 2. WeatherAgent(destination)
    // 3. MapsAgent(routeInfo)
    return `這是 AI Agent 幫你規劃的旅程（根據：${message})`;
}
