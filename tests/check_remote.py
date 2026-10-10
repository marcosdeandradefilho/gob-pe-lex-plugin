"""Exercise a real server using the official MCP client, in both protocol modes."""
import asyncio,json,sys
from contextlib import AsyncExitStack
import httpx2
from mcp.client.streamable_http import streamable_http_client
from mcp import Client
def data(result):
 return result.structured_content or json.loads(result.content[0].text)
async def main():
 url=sys.argv[1] if len(sys.argv)>1 else 'http://127.0.0.1:8765/api/mcp'
 results=[]
 for mode in ['legacy','modern']:
  kwargs={'mode':'legacy'} if mode=='legacy' else {}
  async with AsyncExitStack() as stack:
   if url=='--local':
    from api.mcp import mcp,security
    app=mcp.streamable_http_app(streamable_http_path="/api/mcp",json_response=True,stateless_http=True,transport_security=security)
    await stack.enter_async_context(app.router.lifespan_context(app))
    http=await stack.enter_async_context(httpx2.AsyncClient(transport=httpx2.ASGITransport(app=app)))
    transport=streamable_http_client('http://localhost:8765/api/mcp',http_client=http)
   else:transport=url
   c=await stack.enter_async_context(Client(transport,**kwargs))
   tools=await c.list_tools();names=[t.name for t in tools.tools] if hasattr(tools,'tools') else [t.name for t in tools]
   assert set(names)=={'listar_documentos','buscar_normas','ler_pagina'}
   catalog=await c.call_tool('listar_documentos',{});assert len(data(catalog)['documents'])==9
   found=await c.call_tool('buscar_normas',{'query':'admissão','document_id':'rgf-atualizado-26cd43f5','limit':3});assert data(found)['results']
   hit=data(found)['results'][0];page=await c.call_tool('ler_pagina',{'document_id':hit['document_id'],'page':hit['page']});assert hit['excerpt'] in data(page)['text']
   missing=await c.call_tool('buscar_normas',{'query':'zzzzxxqnoresult'});assert data(missing)['results']==[]
   for arguments in [{'query':'admissão','limit':100},{'query':'a'*301}]:
    bad=await c.call_tool('buscar_normas',arguments);assert bad.is_error
   results.append({'mode':mode,'version':c.protocol_version,'tools':names,'status':'passed'})
 print(json.dumps(results))
asyncio.run(main())
