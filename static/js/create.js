// All needs unit tests

async function createPropertyInputChange(elem){
  const graph_type = elem.getAttribute("graph_type")
  const graph_property = elem.getAttribute("graph_property")
  const search_str = elem.value
  console.log(graph_type, graph_property, search_str)
  let response = await getCandidateEntities(graph_type, graph_property, search_str)
  let candidate_ids = await response.json()
  console.log(candidate_ids)
  return candidate_ids
  // Provide candidates as array of choices
  // Need mui for simple suggestion interface
}

async function getCandidateEntities(type, property, search_str){
  return fetch(`http://localhost:8000/suggest_pointed_entity/?type=${type}&property=${property}&search_str=${search_str}`)
}
