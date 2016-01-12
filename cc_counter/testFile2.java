/**
 *  * Title: SmatDBController.java
 *   * Description:
 *    * Copyright:       NOTICE
 *     * THIS SOFTWARE IS THE PROPERTY OF AND CONTAINS CONFIDENTIAL INFORMATION OF INFOR AND/OR ITS AFFILIATES   
 *      * OR SUBSIDIARIES AND SHALL NOT BE DISCLOSED WITHOUT PRIOR WRITTEN PERMISSION. LICENSED CUSTOMERS MAY
 *       * COPY AND ADAPT THIS SOFTWARE FOR THEIR OWN USE IN ACCORDANCE WITH THE TERMS OF THEIR SOFTWARE LICENSE   
 *        * AGREEMENT.
 *         * ALL OTHER RIGHTS RESERVED.                                                                              
 *          *              
 *           * (c) COPYRIGHT 2015 INFOR.  ALL RIGHTS RESERVED. THE WORD AND DESIGN MARKS SET FORTH HEREIN ARE
 *            * TRADEMARKS AND/OR REGISTERED TRADEMARKS OF INFOR AND/OR ITS AFFILIATES AND SUBSIDIARIES. ALL RIGHTS
 *             * RESERVED.  ALL OTHER TRADEMARKS LISTED HEREIN ARE THE PROPERTY OF THEIR RESPECTIVE OWNERS.
 *              *
 *               * Company: Infor, Inc.
 *                * @author Michael Cao
 *                 * @version $Id$
 *                  */
package com.infor.cloverleaf.api.smatdb.web.rest;

import java.rmi.dgc.VMID;
import java.util.List;
import java.util.Map;

import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import com.hie.cloverleaf.configserver.ConfigServer;
import com.hie.cloverleaf.configserver.SmatClientId;
import com.hie.cloverleaf.configserver.SmatDBConfigServer;
import com.hie.cloverleaf.configserver.smat.search.AliasItemList;
import com.hie.cloverleaf.configserver.smat.search.IndexedFile;
import com.hie.cloverleaf.configserver.smat.search.SearchResult;
import com.hie.cloverleaf.configserver.smatdb.ResendResult;
import com.hie.cloverleaf.install.CriteriaDefINI;
import com.infor.cloverleaf.api.domain.smatdb.CloverResendMessageContext;
import com.infor.cloverleaf.api.domain.smatdb.CloverSearchMessageContext;
import com.infor.cloverleaf.api.domain.smatdb.CloverSmatMessage;
import com.infor.cloverleaf.api.web.AbstractCloverleafController;

@RestController
@RequestMapping(value = { "/site/{siteName}/smatdb", "/api/site/{siteName}/smatdb" })
public class SmatDBController extends AbstractCloverleafController {
    
    public static final String PARAM_BASE_NODE = "baseNode";
    private SmatClientId _clientId;
   
    protected SmatDBConfigServer getSmatDBConfigServer(String siteName) throws Exception {
        ConfigServer configServer = getConfigServer(siteName);
        return configServer.getSmatDBConfigServer();
    }

    @RequestMapping(value = "/aliasSettings", method = RequestMethod.GET)
    public AliasItemList getAliasSettingList(@PathVariable("siteName") String siteName) throws Exception {
        return null;
    }
    
    @RequestMapping(value = "/aliasSettings", method = RequestMethod.POST)
    public void saveAliasSettingList(@PathVariable("siteName") String siteName, @RequestBody AliasItemList aliasSettings) throws Exception {
    }
    
    @RequestMapping(value = "/criteriadefinition", method = RequestMethod.GET)
    public CriteriaDefINI getCriteriaDefINI(@PathVariable("siteName") String siteName) throws Exception {
        return null;
    }
    
    @RequestMapping(value = "/criteriadefinition", method = RequestMethod.POST)
    public void saveCriteriaDefINI(@PathVariable("siteName") String siteName, @RequestBody CriteriaDefINI definition) throws Exception {
    }
    
    /**
 *      * Find smat database file by file name.
 *           * 
 *                * @param siteName
 *                     * @param processName
 *                          * @param params
 *                               * @return
 *                                    * @throws Exception
 *                                         */
    @RequestMapping(value = "/indexedfile/process/{processName}", method = RequestMethod.GET)
    public IndexedFile getDBIndexedFile(@PathVariable("siteName") String siteName, @PathVariable("processName") String processName, @RequestParam Map<String, String> params) throws Exception {
        String file = params.get(PARAM_FILE);
        return null;
    }
    
    @RequestMapping(value = "/indexedfiles", method = RequestMethod.GET)
    public List<IndexedFile> getDBIndexedFiles(@PathVariable("siteName") String siteName) throws Exception {
        return null;
    }
    
    @RequestMapping(value = "/indexedfiles/process/{processName}", method = RequestMethod.GET)
    public Map<String, List<IndexedFile>> getDBIndexedFiles(@PathVariable("siteName") String siteName, @PathVariable("processName") String processName) throws Exception {
        return null;
    }
    
    @RequestMapping(value = "/rexrep/format/{format}", method = RequestMethod.GET)
    public IndexedFile getJavaRexRep(@PathVariable("siteName") String siteName, @PathVariable("format") int format, @RequestParam Map<String, String> params) throws Exception {
        String baseNode = params.get(PARAM_BASE_NODE);
        return null;
    }
    
    @RequestMapping(value = "/message", method = RequestMethod.GET)
    public CloverSmatMessage getSmatMsg(@PathVariable("siteName") String siteName, @RequestParam Map<String, String> params) throws Exception {
        //TODO: based on parameters, invoke related getSmatMsg or getSmatNewFormatMessage
        //        return null;
        //            }
        //
        //                @RequestMapping(value = "/resend", method = RequestMethod.POST)
        //                    public ResendResult resendMessages(@PathVariable("siteName") String siteName, @RequestBody CloverResendMessageContext context) throws Exception {
        //                            return null;
        //                                }
        //                                    
        //                                        @RequestMapping(value = "/search", method = RequestMethod.GET)
        //                                            public SearchResult searchMessages(@PathVariable("siteName") String siteName, @RequestBody CloverSearchMessageContext context) throws Exception {
        //                                                	ConfigServer configServer = getConfigServer(siteName);
        //                                                	    	SearchResult result = configServer.getSmatDBConfigServer().searchMessages(getSMATClientId(), context.to(), context.getMsgNumPerPage(), context.getPageNum());
        //                                                	    	    	return result;
        //                                                	    	    	    }
        //                                                	    	    	        
        //                                                	    	    	            private synchronized SmatClientId getSMATClientId() {
        //                                                	    	    	                    if (_clientId == null)
        //                                                	    	    	                                _clientId = new SmatClientId(new VMID(), "SMAT Restful API");
        //                                                	    	    	                                        return _clientId;
        //                                                	    	    	                                            }
        //                                                	    	    	                                            }
