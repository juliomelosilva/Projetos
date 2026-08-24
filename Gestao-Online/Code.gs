/**
 * GESTÃO ON-LINE — API Google Apps Script
 *
 * Cole este arquivo no projeto Apps Script vinculado à planilha usada pelo sistema.
 * Depois publique como Aplicativo da Web:
 * - Executar como: você
 * - Quem tem acesso: qualquer pessoa com o link (ou a opção equivalente disponível)
 *
 * A planilha funciona como banco compartilhado para todos os navegadores/dispositivos.
 */

const SHEET_NAME = 'GestaoOnline';

function doGet(e) {
  // GET serve para teste e saúde da API. A aplicação usa POST para load/sync.
  return json_({ok:true, service:'Gestão On-line API', version:'1.1', time:new Date().toISOString()});
}

function doPost(e) {
  try {
    const body = JSON.parse((e && e.postData && e.postData.contents) || '{}');
    if (body.action === 'sync') {
      saveSnapshot_(body.data || {});
      return json_({ok:true, action:'sync'});
    }
    if (body.action === 'load') {
      return json_({ok:true, action:'load', data:loadSnapshot_()});
    }
    return json_({ok:false,error:'Ação não reconhecida'});
  } catch (err) {
    return json_({ok:false,error:String(err)});
  }
}

function getSheet_() {
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  let sh = ss.getSheetByName(SHEET_NAME);
  if (!sh) {
    sh = ss.insertSheet(SHEET_NAME);
    sh.getRange(1,1,1,3).setValues([['chave','atualizado_em','json']]);
    sh.setFrozenRows(1);
  }
  return sh;
}

function saveSnapshot_(data) {
  const sh = getSheet_();
  const json = JSON.stringify(data);
  sh.getRange(2,1,1,3).setValues([['snapshot',new Date(),json]]);
  SpreadsheetApp.flush();
}

function loadSnapshot_() {
  const sh = getSheet_();
  if (sh.getLastRow() < 2) return {};
  const value = sh.getRange(2,3).getValue();
  if (!value) return {};
  try { return JSON.parse(value); }
  catch (err) { throw new Error('Snapshot inválido na planilha: ' + err); }
}

function json_(obj) {
  return ContentService
    .createTextOutput(JSON.stringify(obj))
    .setMimeType(ContentService.MimeType.JSON);
}
