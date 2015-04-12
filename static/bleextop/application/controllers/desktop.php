<?php if ( ! defined('BASEPATH')) exit('No direct script access allowed');

class Desktop extends Bleext_Controller {


	public function index()
	{
		$this->load->view('desktop');
	}
	
	public function home(){
		$this->load->view('desktop');
	}
	
	public function config(){
		$this->load->library("applicationbi");

		$this->response(true,array(
			"dock"		=> "top",
			"user"		=> $this->getUser(),
			"config"	=> array(
				"wallpaper"	=> "static/bleextop/resources/wallpapers/background.png"
			),
			"applications"	=> $this->applicationbi->getApplications($this->getUser())
		));
	}
}
