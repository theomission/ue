require 'ue_file_utils'

include UeFileUtils

class Element
  include Mongoid::Document
  include Mongoid::Timestamps

  field :elclass,    :type => String
  field :eltype,     :type => String
  field :elname,     :type => String
  field :path,       :type => String
  field :created_by, :type => String

  belongs_to :asset
  embeds_many :versions

  after_save :create_dirs
  after_initialize do
    self.path = get_path
  end

  def Element.get_element(project, group, asset, elclass, eltype, elname)
    a = Asset.get_asset(project, group, asset)
    if a == {} || a == nil
      return {}
    else
      e = a.elements.where(:elclass => elclass, :eltype => eltype, :elname => elname).first
      if e == nil
        return {}
      else
        return e
      end
    end
  end

  def Element.get_elements(project, group, asset)
    a = Asset.get_asset(project, group, asset)
    if a == {} || a == nil
      return []
    else
      return a.elements
    end
  end

  private

  def get_path
    if self.path.nil?
      UeFileUtils::get_element_path self.asset.path, self.elclass, self.eltype, self.elname
    else
      self.path
    end
  end

  def create_dirs
    UeFileUtils::create_dir get_path
  end
end
