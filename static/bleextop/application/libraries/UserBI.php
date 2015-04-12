<?php

require_once('static/bleextop/application/core/BleextBI'.EXT);

class UserBI extends BleextBI{
	
	function UserBI(){
		parent::BleextBI();
		
		$this->instance->load->model("userdao");
	}
	
	public function getAll(){
		return $this->instance->userdao->getAll();
	}
	
	public function save($form){
		
	}
	
}