/**
 *  * Title: HmdController.java
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
package com.infor.cloverleaf.api.formats.web.rest;

import java.util.List;
import java.util.Map;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;
import org.springframework.web.bind.annotation.ResponseBody;
import org.springframework.web.bind.annotation.RestController;

import com.infor.cloverleaf.api.domain.formats.CloverHmdDefinition;
import com.infor.cloverleaf.api.domain.formats.CloverHmdMessage;
import com.infor.cloverleaf.api.domain.formats.CloverHmdSegment;
import com.infor.cloverleaf.api.exception.InvalidRequestException;
import com.infor.cloverleaf.api.formats.service.HmdService;
import com.infor.cloverleaf.api.web.AbstractCloverleafController;

import io.swagger.annotations.Api;

@Api("HMD API")
@RestController
@RequestMapping(value = {"/api/format/hmd"})
public class HmdController extends AbstractCloverleafController {
	
	@Autowired
	private HmdService hmdService;
	
	@RequestMapping(value = "/{formatName}/versions", method = RequestMethod.GET)
	public @ResponseBody List<String> listVersions(@PathVariable("formatName") String formatName) throws InvalidRequestException {
		try {
			return hmdService.listVersions(formatName);
		} catch (Exception e) {
			throw new InvalidRequestException(e.getMessage());
		}
	}
	
	@RequestMapping(value = "/{formatName}/{version}/message", method = RequestMethod.POST)
	public @ResponseBody Map<String, List<String[]>> parseMessage(@PathVariable("formatName") String formatName, @PathVariable("version") String formatVersion, @RequestBody String content) {
		return hmdService.parseMessage(formatName, formatVersion, content);
	}
	
	@RequestMapping(value = "/{formatName}/{version}", method = RequestMethod.GET)
	public CloverHmdDefinition getHmdDefinition(@PathVariable("formatName") String formatName, @PathVariable("version") String version) {
		try {
			return hmdService.getHmdDefinition(formatName, version);
		} catch (Exception e) {
			throw new InvalidRequestException(e.getMessage());
		}
	}
	
	@RequestMapping(value = "/{formatName}/{version}/message/{messageName}", method = RequestMethod.GET)
	public CloverHmdMessage getHmdMessage(@PathVariable("formatName") String formatName, @PathVariable("version") String version, @PathVariable("messageName") String messageName) {
		try {
			return hmdService.getHmdMessage(formatName, version, messageName);
		} catch (Exception e) {
			throw new InvalidRequestException(e.getMessage());
		}
	}

	@RequestMapping(value = "/{formatName}/{version}/segment/{segmentName}", method = RequestMethod.GET)
	public CloverHmdSegment getHmdSegment(@PathVariable("formatName") String formatName, @PathVariable("version") String version, @PathVariable("segmentName") String segmentName) {
		try {
			return hmdService.getHmdSegment(formatName, version, segmentName);
		} catch (Exception e) {
			throw new InvalidRequestException(e.getMessage());
		}
	}
}
