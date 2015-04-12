<?php


require_once('static/bleextop/application/core/BleextBI'.EXT);

class ApplicationBI extends BleextBI{
	
	function ApplicationBI(){
		parent::BleextBI();
		
		$this->instance->load->model("applicationdao");
		$this->appdao = $this->instance->applicationdao;
	}
	
	public function getApplications($params){
		
		$apps = $this->appdao->getApplications($params);
		
		$tree = $this->buildTree($apps,"menu");
		
		return $tree->getRoot();

	}
	
	public function getTree(){
		
		$apps = $this->appdao->getAll();
		
		$tree = $this->buildTree($apps,"children");
		
		return $tree->getRoot();
	}
	
	public function save($form){
		$form->date_updated = date("Y-m-d h:i:s");
		$form->date_created = date("Y-m-d h:i:s");
		$id = $this->appdao->save($form);
		
		if($id === false){
			return array("success"=>false,"message"=>"There was an error saving this application.");
		}else{
			$this->appdao->addPermissions($id);
			
			return array("success"=>true,"application_k"=>$id,"message"=>"Application successfully saved");
		}
	}
	
	public function update($form){
		$form->date_updated = date("Y-m-d h:i:s");
		$success = $this->appdao->update($form);
		
		if($success){
			return array("success"=>true,"application_k"=>$form->application_k,"message"=>"Application successfully updated");
		}else{
			return array("success"=>false,"message"=>"There was an error updating this application.");
		}
	}
	
	public function remove($application_k){
		$this->appdao->remove($application_k);
	}
	
	public function move($form){
		$success = $this->appdao->move($form);
		if($success){
			return array("success"=>true,"message"=>"Application successfully moved");
		}else{
			return array("success"=>false,"message"=>"There was an error moving this application.");
		}
	}
	
	private function buildTree($apps,$text){
		$CI =& get_instance();
		$CI->load->library("tree");
		
		$temp = array();
		foreach($apps as $app){
			$iconCls = "";
			if($app["configurations"]){
				$conf = json_decode($app["configurations"]);
				if($conf){
					if(property_exists($conf,"iconCls")){
						$iconCls = $conf->iconCls;
					}
				}
			}
			array_push($temp,array(
				"text"			=> $app["name"],
				"name"			=> $app["name"],
				"application_k"	=> $app["application_k"],
				"application_parent_k"=> $app["application_parent_k"],
				"klass"			=> $app["klass"],
				"description"	=> $app["description"],
				"configurations"=> $app["configurations"],
				"active"		=> $app["active"],
				"iconCls"		=> $iconCls
			));
		}
		
		// Creating the Tree
		$tree = new Tree();
		$tree->setChildProperty($text);
		$tree->setIdProperty("application_k");
		foreach($temp as $app){
			$tree->addChild($app,$app["application_parent_k"]);
		}
		return $tree;
	}
}