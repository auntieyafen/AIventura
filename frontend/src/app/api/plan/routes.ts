import { NextRequest, NextResponse } from "next/server";
import { handleAgentPlan } from "@/libs/agents";

export async function POST(req: NextRequest) {
    const body = await req.json();
    const message = body.message;

    const plan = await handleAgentPlan(message); // 呼叫 Agent
    return NextResponse.json({ plan });
}