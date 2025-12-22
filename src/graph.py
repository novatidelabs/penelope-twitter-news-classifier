"""LangGraph workflow for Twitter News Classification."""

from langgraph.graph import END, START, StateGraph
from src.models.state import AnalysisState
from src.api.client import APIClient

# Signal Integrity Agents
from src.agents.specialized.sarcasm_sentinel_agent.agent import sarcasm_sentinel_agent
from src.agents.specialized.echo_mapper_agent.agent import echo_mapper_agent
from src.agents.specialized.latency_guard_agent.agent import latency_guard_agent
from src.agents.specialized.slop_filter_agent.agent import slop_filter_agent
from src.agents.specialized.banned_phrase_skeptic_agent.agent import banned_phrase_skeptic_agent

# Core Analysis Agents
from src.agents.specialized.summary_agent.agent import summary_agent
from src.agents.specialized.input_preprocessor_agent.agent import input_preprocessor_agent
from src.agents.specialized.context_evaluator_agent.agent import context_evaluator_agent
from src.agents.specialized.fact_checker_agent.agent import fact_checker_agent
from src.agents.specialized.depth_analyzer_agent.agent import depth_analyzer_agent
from src.agents.specialized.relevance_analyzer_agent.agent import relevance_analyzer_agent
from src.agents.specialized.structure_analyzer_agent.agent import structure_analyzer_agent
from src.agents.specialized.reflective_agent.agent import reflective_agent
from src.agents.specialized.metadata_ranker_agent.agent import metadata_ranker_agent
from src.agents.specialized.consensus_agent.agent import consensus_agent
from src.agents.specialized.score_consolidator_agent.agent import score_consolidator_agent
from src.agents.specialized.validator_agent.agent import validator_agent


def create_graph(api_client: APIClient):
    """Create and compile the LangGraph workflow."""
    builder = StateGraph(AnalysisState)
    
    # Signal Integrity nodes
    async def sarcasm_node(state: AnalysisState):
        return await sarcasm_sentinel_agent(state, api_client)
    
    async def echo_node(state: AnalysisState):
        return await echo_mapper_agent(state, api_client)
    
    async def latency_node(state: AnalysisState):
        return await latency_guard_agent(state, api_client)
    
    async def slop_node(state: AnalysisState):
        return await slop_filter_agent(state, api_client)
    
    async def banned_phrase_node(state: AnalysisState):
        return await banned_phrase_skeptic_agent(state, api_client)
    
    # Core Analysis nodes
    async def summary_node(state: AnalysisState):
        return await summary_agent(state, api_client)
    
    async def preprocessing_node(state: AnalysisState):
        return await input_preprocessor_agent(state, api_client)
    
    async def context_node(state: AnalysisState):
        return await context_evaluator_agent(state, api_client)
    
    async def fact_check_node(state: AnalysisState):
        return await fact_checker_agent(state, api_client)
    
    async def depth_node(state: AnalysisState):
        return await depth_analyzer_agent(state, api_client)
    
    async def relevance_node(state: AnalysisState):
        return await relevance_analyzer_agent(state, api_client)
    
    async def structure_node(state: AnalysisState):
        return await structure_analyzer_agent(state, api_client)
    
    async def reflection_node(state: AnalysisState):
        return await reflective_agent(state, api_client)
    
    async def metadata_node(state: AnalysisState):
        return await metadata_ranker_agent(state, api_client)
    
    async def consensus_node(state: AnalysisState):
        return await consensus_agent(state, api_client)
    
    async def score_consolidation_node(state: AnalysisState):
        return await score_consolidator_agent(state, api_client)
    
    async def validation_node(state: AnalysisState):
        return await validator_agent(state, api_client)
    
    builder.add_node("sarcasm_detection", sarcasm_node)
    builder.add_node("echo_mapping", echo_node)
    builder.add_node("latency_guard", latency_node)
    builder.add_node("slop_filter", slop_node)
    builder.add_node("banned_phrase_check", banned_phrase_node)
    
    builder.add_node("summary", summary_node)
    builder.add_node("preprocessing", preprocessing_node)
    builder.add_node("context_evaluation", context_node)
    builder.add_node("fact_check", fact_check_node)
    builder.add_node("depth_analysis", depth_node)
    builder.add_node("relevance_analysis", relevance_node)
    builder.add_node("structure_analysis", structure_node)
    builder.add_node("reflection", reflection_node)
    builder.add_node("metadata_ranking", metadata_node)
    builder.add_node("consensus", consensus_node)
    builder.add_node("score_consolidation", score_consolidation_node)
    builder.add_node("validation", validation_node)
    
    # Signal Integrity flow
    builder.add_edge(START, "sarcasm_detection")
    builder.add_edge("sarcasm_detection", "echo_mapping")
    builder.add_edge("echo_mapping", "latency_guard")
    builder.add_edge("latency_guard", "slop_filter")
    builder.add_edge("slop_filter", "banned_phrase_check")
    
    # Conditional: continue to core analysis if quality passes
    def should_continue(state: AnalysisState) -> str:
        return "continue" if state.get("quality_pass", True) else "end"
    
    builder.add_conditional_edges(
        "banned_phrase_check",
        should_continue,
        {
            "continue": "summary",
            "end": END
        }
    )
    
    # Core Analysis flow
    builder.add_edge("summary", "preprocessing")
    builder.add_edge("preprocessing", "context_evaluation")
    builder.add_edge("context_evaluation", "fact_check")
    builder.add_edge("fact_check", "depth_analysis")
    builder.add_edge("depth_analysis", "relevance_analysis")
    builder.add_edge("relevance_analysis", "structure_analysis")
    builder.add_edge("structure_analysis", "reflection")
    builder.add_edge("reflection", "metadata_ranking")
    builder.add_edge("metadata_ranking", "consensus")
    builder.add_edge("consensus", "score_consolidation")
    builder.add_edge("score_consolidation", "validation")
    builder.add_edge("validation", END)
    
    return builder.compile()


# Default graph instance for LangGraph Studio
from src.api.client import APIClient

_default_api_client = APIClient()
graph = create_graph(_default_api_client)

