"""Synthetic NF-e v4.00 fixture (schema-accurate; verified against a real NF-e during build)."""
NFe_V400 = """<?xml version="1.0" encoding="UTF-8"?>
<NFe xmlns="http://www.portalfiscal.inf.br/nfe">
  <infNFe Id="NFe35260812345678000190550010000000011000000019" versao="4.00">
    <ide>
      <cUF>35</cUF><cNF>00000001</cNF><natOp>VENDA</natOp>
      <mod>55</mod><serie>1</serie><nNF>1</nNF>
      <dhEmi>2026-08-10T14:30:00-03:00</dhEmi>
      <tpNF>1</tpNF><idDest>1</idDest><cMunFG>3550308</cMunFG>
      <tpImp>1</tpImp><tpEmis>1</tpEmis><cDV>1</cDV><tpAmb>2</tpAmb>
      <finNFe>1</finNFe><indFinal>1</indFinal><indPres>1</indPres>
      <procEmi>0</procEmi><verProc>TESTE-1.0</verProc>
    </ide>
    <emit>
      <CNPJ>12345678000190</CNPJ><xNome>EMPRESA TESTE LTDA</xNome>
      <xFant>TESTE</xFant><IE>123456789</IE><CRT>3</CRT>
    </emit>
    <dest>
      <CPF>98765432100</CPF><xNome>CLIENTE TESTE</xNome>
      <indIEDest>9</indIEDest>
    </dest>
    <det nItem="1">
      <prod>
        <cProd>P001</cProd><cEAN>SEM GTIN</cEAN>
        <xProd>PRESTACAO DE SERVICO DE DESENVOLVIMENTO</xProd>
        <NCM>00000000</NCM><CFOP>5949</CFOP><uCom>UN</uCom><qCom>1.0000</qCom>
        <vUnCom>2500.00</vUnCom><vProd>2500.00</vProd><cEANTrib>SEM GTIN</cEANTrib>
        <uTrib>UN</uTrib><qTrib>1.0000</qTrib><vUnTrib>2500.00</vUnTrib>
        <indTot>1</indTot>
      </prod>
    </det>
    <det nItem="2">
      <prod>
        <cProd>P002</cProd><cEAN>SEM GTIN</cEAN>
        <xProd>HOSPEDAGEM DE SISTEMA</xProd>
        <NCM>00000000</NCM><CFOP>5949</CFOP><uCom>UN</uCom><qCom>1.0000</qCom>
        <vUnCom>500.00</vUnCom><vProd>500.00</vProd><cEANTrib>SEM GTIN</cEANTrib>
        <uTrib>UN</uTrib><qTrib>1.0000</qTrib><vUnTrib>500.00</vUnTrib>
        <indTot>1</indTot>
      </prod>
    </det>
    <total>
      <ICMSTot>
        <vBC>0.00</vBC><vICMS>0.00</vICMS><vICMSDeson>0.00</vICMSDeson>
        <vFCP>0.00</vFCP><vBCST>0.00</vBCST><vST>0.00</vST><vFCPST>0.00</vFCPST>
        <vFCPSTRet>0.00</vFCPSTRet><vProd>3000.00</vProd><vFrete>0.00</vFrete>
        <vSeg>0.00</vSeg><vDesc>0.00</vDesc><vII>0.00</vII><vIPI>0.00</vIPI>
        <vIPIDevol>0.00</vIPIDevol><vPIS>0.00</vPIS><vCOFINS>0.00</vCOFINS>
        <vOutro>0.00</vOutro><vNF>3000.00</vNF>
      </ICMSTot>
    </total>
    <pag><detPag><tPag>01</tPag><vPag>3000.00</vPag></detPag></pag>
    <infAdic><infCpl>NOTA FISCAL DE TESTE</infCpl></infAdic>
  </infNFe>
</NFe>
"""
