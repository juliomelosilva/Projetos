/**
 * GESTÃO ON-LINE — Google Apps Script
 *
 * IMPORTANTE:
 * 1. Cole este arquivo no projeto Google Apps Script ligado à planilha.
 * 2. Crie/seleciona uma planilha para armazenamento.
 * 3. Implante como Web App: executar como você / acesso conforme sua necessidade.
 *
 * O frontend já está apontando para o endpoint informado pelo usuário.
 */

const SHEET_NAME = 'GestaoOnline';

function doGet(e) {
  return json_({ok:true, service:'Gestão On-line API', time:new Date().toISOString()});
}

function doPost(e) {
  try {
    const body = JSON.parse(e.postData.contents || '{}');
    if (body.action === 'sync') {
      saveSnapshot_(body.data || {});
      return json_({ok:true, action:'sync'});
    }
    if (body.action === 'load') {
      return json_({ok:true, data:loadSnapshot_()});
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
  }
  return sh;
}

function saveSnapshot_(data) {
  const sh = getSheet_();
  const json = JSON.stringify(data);
  sh.getRange(2,1,1,3).setValues([['snapshot',new Date(),json]]);
}

function loadSnapshot_() {
  const sh = getSheet_();
  if (sh.getLastRow() < 2) return {};
  const value = sh.getRange(2,3).getValue();
  return value ? JSON.parse(value) : {};
}

function json_(obj) {
  return ContentService
    .createTextOutput(JSON.stringify(obj))
    .setMimeType(ContentService.MimeType.JSON);
}
